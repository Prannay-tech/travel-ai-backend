"""
Enhanced FastAPI backend for Travel AI application with real-world data integration.
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import os
import sys
from datetime import datetime, timedelta

# Add the etl directory to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'etl'))

from embed import TravelEmbedder
from load_supabase import SupabaseLoader
from config import settings
from services.recommendation_service import recommendation_service
from clients.currency_client import currency_client
from clients.weather_client import weather_client
from clients.holiday_client import holiday_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Travel AI API",
    description="AI-powered travel recommendation and search API with real-world data integration",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
embedder = TravelEmbedder()

# Load Supabase configuration from environment
if settings.SUPABASE_URL and settings.SUPABASE_KEY:
    supabase_loader = SupabaseLoader(settings.SUPABASE_URL, settings.SUPABASE_KEY)
else:
    supabase_loader = None
    logger.warning("Supabase credentials not configured")

# Pydantic models for enhanced API
class TravelPreferencesRequest(BaseModel):
    destination: str
    budget: Optional[str] = None
    travelDates: Optional[str] = None
    currentLocation: Optional[str] = None
    preferences: Optional[str] = None
    currency: str = "USD"
    travelType: str = "international"

class CurrencyConversionRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str

class WeatherRequest(BaseModel):
    location: str
    days: Optional[int] = 3

class HolidayRequest(BaseModel):
    country: str
    year: Optional[int] = None
    month: Optional[int] = None

class EnhancedRecommendationResponse(BaseModel):
    places: List[Dict[str, Any]]
    weather: Optional[Dict[str, Any]]
    holidays: List[Dict[str, Any]]
    summary: Dict[str, Any]

class CurrencyResponse(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
    converted_amount: float
    rate: float

class WeatherResponse(BaseModel):
    location: Dict[str, Any]
    current: Dict[str, Any]
    forecast: List[Dict[str, Any]]

class HolidayResponse(BaseModel):
    holidays: List[Dict[str, Any]]
    country: str
    year: int

# Dependency to check if Supabase is available
def get_supabase():
    if supabase_loader is None:
        raise HTTPException(status_code=503, detail="Database not configured")
    return supabase_loader

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Travel AI API v2.0",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "Real-world destination data",
            "Currency conversion",
            "Weather integration",
            "Holiday information",
            "Domestic/International travel options"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database_connected": supabase_loader is not None,
        "api_keys_configured": {
            "weather": bool(settings.WEATHER_API_KEY),
            "holidays": bool(settings.CALENDARIFIC_API_KEY),
            "currency": bool(settings.EXCHANGERATE_API_KEY),
            "tomtom": bool(settings.TOMTOM_API_KEY),
            "amadeus": bool(settings.AMADEUS_CLIENT_ID and settings.AMADEUS_CLIENT_SECRET)
        }
    }

@app.post("/recommendations/enhanced", response_model=EnhancedRecommendationResponse)
async def get_enhanced_recommendations(request: TravelPreferencesRequest):
    """Get enhanced travel recommendations with real-world data."""
    try:
        logger.info(f"Generating enhanced recommendations for: {request.destination}")
        
        # Convert request to dict
        travel_data = request.dict()
        
        # Generate recommendations using the service
        recommendations = await recommendation_service.generate_recommendations(travel_data)
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error generating enhanced recommendations: {e}")
        raise HTTPException(status_code=500, detail="Error generating recommendations")

@app.post("/currency/convert", response_model=CurrencyResponse)
async def convert_currency(request: CurrencyConversionRequest):
    """Convert currency using real-time rates."""
    try:
        converted_amount = await currency_client.convert_currency(
            request.amount, request.from_currency, request.to_currency
        )
        
        if converted_amount is None:
            raise HTTPException(status_code=400, detail="Currency conversion failed")
        
        # Get the exchange rate
        rates = await currency_client.get_exchange_rates(request.from_currency)
        rate = rates.get(request.to_currency, 1.0)
        
        return CurrencyResponse(
            from_currency=request.from_currency,
            to_currency=request.to_currency,
            amount=request.amount,
            converted_amount=converted_amount,
            rate=rate
        )
        
    except Exception as e:
        logger.error(f"Error converting currency: {e}")
        raise HTTPException(status_code=500, detail="Currency conversion error")

@app.get("/currency/rates")
async def get_exchange_rates(base_currency: str = "USD"):
    """Get current exchange rates for all supported currencies."""
    try:
        rates = await currency_client.get_exchange_rates(base_currency)
        return {
            "base_currency": base_currency,
            "rates": rates,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting exchange rates: {e}")
        raise HTTPException(status_code=500, detail="Error fetching exchange rates")

@app.get("/currency/supported")
async def get_supported_currencies():
    """Get list of supported currencies."""
    currencies = await currency_client.get_supported_currencies()
    return {
        "currencies": currencies,
        "count": len(currencies)
    }

@app.post("/weather/current", response_model=WeatherResponse)
async def get_current_weather(request: WeatherRequest):
    """Get current weather for a location."""
    try:
        weather_data = await weather_client.get_current_weather(request.location)
        
        if weather_data is None:
            raise HTTPException(status_code=404, detail="Weather data not found")
        
        return WeatherResponse(
            location=weather_data["location"],
            current=weather_data["current"],
            forecast=[]
        )
        
    except Exception as e:
        logger.error(f"Error getting weather: {e}")
        raise HTTPException(status_code=500, detail="Error fetching weather data")

@app.post("/weather/forecast", response_model=WeatherResponse)
async def get_weather_forecast(request: WeatherRequest):
    """Get weather forecast for a location."""
    try:
        forecast_data = await weather_client.get_forecast(request.location, request.days or 3)
        
        if forecast_data is None:
            raise HTTPException(status_code=404, detail="Forecast data not found")
        
        return WeatherResponse(
            location=forecast_data["location"],
            current=forecast_data["current"],
            forecast=forecast_data["forecast"]
        )
        
    except Exception as e:
        logger.error(f"Error getting forecast: {e}")
        raise HTTPException(status_code=500, detail="Error fetching forecast data")

@app.post("/weather/summary", response_model=WeatherResponse)
async def get_weather_summary(request: WeatherRequest):
    """Get comprehensive weather summary including current and forecast."""
    try:
        weather_summary = await weather_client.get_weather_summary(request.location)
        
        if weather_summary is None:
            raise HTTPException(status_code=404, detail="Weather summary not found")
        
        return WeatherResponse(
            location=weather_summary["location"],
            current=weather_summary["current"],
            forecast=weather_summary["forecast"]
        )
        
    except Exception as e:
        logger.error(f"Error getting weather summary: {e}")
        raise HTTPException(status_code=500, detail="Error fetching weather summary")

@app.post("/holidays", response_model=HolidayResponse)
async def get_holidays(request: HolidayRequest):
    """Get holidays for a specific country."""
    try:
        year = request.year or datetime.now().year
        holidays = await holiday_client.get_holidays(request.country, year, request.month)
        
        if holidays is None:
            raise HTTPException(status_code=404, detail="Holiday data not found")
        
        return HolidayResponse(
            holidays=holidays,
            country=request.country,
            year=year
        )
        
    except Exception as e:
        logger.error(f"Error getting holidays: {e}")
        raise HTTPException(status_code=500, detail="Error fetching holiday data")

@app.get("/holidays/upcoming")
async def get_upcoming_holidays(
    country: str = Query(..., description="Country code"),
    days_ahead: int = Query(90, description="Number of days to look ahead")
):
    """Get upcoming holidays within the next N days."""
    try:
        holidays = await holiday_client.get_upcoming_holidays(country, days_ahead)
        
        if holidays is None:
            raise HTTPException(status_code=404, detail="Upcoming holidays not found")
        
        return {
            "country": country,
            "days_ahead": days_ahead,
            "holidays": holidays,
            "count": len(holidays)
        }
        
    except Exception as e:
        logger.error(f"Error getting upcoming holidays: {e}")
        raise HTTPException(status_code=500, detail="Error fetching upcoming holidays")

@app.get("/destinations/domestic")
async def get_domestic_destinations():
    """Get list of domestic US destinations."""
    try:
        destinations = recommendation_service.domestic_destinations
        return {
            "travel_type": "domestic",
            "destinations": destinations,
            "categories": list(destinations.keys())
        }
    except Exception as e:
        logger.error(f"Error getting domestic destinations: {e}")
        raise HTTPException(status_code=500, detail="Error fetching domestic destinations")

@app.get("/destinations/international")
async def get_international_destinations():
    """Get list of international destinations."""
    try:
        destinations = recommendation_service.international_destinations
        return {
            "travel_type": "international",
            "destinations": destinations,
            "categories": list(destinations.keys())
        }
    except Exception as e:
        logger.error(f"Error getting international destinations: {e}")
        raise HTTPException(status_code=500, detail="Error fetching international destinations")

@app.get("/destinations/search")
async def search_destinations(
    travel_type: str = Query(..., description="domestic or international"),
    destination_type: str = Query(None, description="beach, mountain, city"),
    budget_max: Optional[float] = Query(None, description="Maximum budget in USD"),
    currency: str = Query("USD", description="Currency for cost display")
):
    """Search destinations by criteria."""
    try:
        # Get destination pool
        if travel_type == "domestic":
            destination_pool = recommendation_service.domestic_destinations
        elif travel_type == "international":
            destination_pool = recommendation_service.international_destinations
        else:
            raise HTTPException(status_code=400, detail="Invalid travel type")
        
        # Filter by destination type
        if destination_type:
            if destination_type in destination_pool:
                selected = destination_pool[destination_type]
            else:
                selected = []
        else:
            # Mix of all types
            selected = []
            for category in destination_pool.values():
                selected.extend(category)
        
        # Filter by budget
        if budget_max:
            selected = [
                dest for dest in selected 
                if dest["cost_day_usd"] * 7 + dest["avg_flight_cost"] <= budget_max
            ]
        
        # Convert costs to selected currency
        converted_destinations = await recommendation_service._convert_destination_costs(
            selected, currency
        )
        
        return {
            "travel_type": travel_type,
            "destination_type": destination_type,
            "currency": currency,
            "destinations": converted_destinations,
            "count": len(converted_destinations)
        }
        
    except Exception as e:
        logger.error(f"Error searching destinations: {e}")
        raise HTTPException(status_code=500, detail="Error searching destinations")

# Legacy endpoints for backward compatibility
@app.post("/recommendations", response_model=EnhancedRecommendationResponse)
async def get_travel_recommendations_legacy(request: TravelPreferencesRequest):
    """Legacy endpoint - redirects to enhanced recommendations."""
    return await get_enhanced_recommendations(request)

if __name__ == "__main__":
    import uvicorn
    
    # Validate required configuration
    missing_keys = settings.validate_required_keys()
    if missing_keys:
        logger.warning(f"Missing required configuration keys: {missing_keys}")
    
    uvicorn.run(
        "main_enhanced:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    ) 