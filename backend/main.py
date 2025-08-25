"""
FastAPI backend for Travel AI application.
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
import random # Added for flight deal mock

# Add the etl directory to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'etl'))

from embed import TravelEmbedder
from load_supabase import SupabaseLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Travel AI API",
    description="AI-powered travel recommendation and search API",
    version="1.0.0"
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
supabase_url = os.getenv("SUPABASE_URL", "")
supabase_key = os.getenv("SUPABASE_KEY", "")

if supabase_url and supabase_key:
    supabase_loader = SupabaseLoader(supabase_url, supabase_key)
else:
    supabase_loader = None
    logger.warning("Supabase credentials not configured")

# Pydantic models
class PlaceSearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10
    min_rating: Optional[float] = 0.0
    location: Optional[str] = None

class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    departure_date: str
    return_date: Optional[str] = None
    adults: Optional[int] = 1
    children: Optional[int] = 0

class TravelRecommendationRequest(BaseModel):
    user_preferences: str
    budget: Optional[float] = None
    duration: Optional[int] = None
    interests: Optional[List[str]] = None

class DestinationRecommendationRequest(BaseModel):
    type: Optional[str] = None  # beach, mountain, city, etc.
    budget: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    stay_type: Optional[str] = None  # hotel, airbnb, resort
    activities: Optional[List[str]] = None
    limit: Optional[int] = 10

class PlaceResponse(BaseModel):
    place_id: str
    name: str
    type: str
    categories: str
    latitude: Optional[float]
    longitude: Optional[float]
    country: str
    city: str
    rate: float
    description: str
    image: Optional[str]
    similarity_score: Optional[float]

class FlightResponse(BaseModel):
    quote_id: str
    min_price: float
    currency: str
    direct: bool
    origin_id: str
    destination_id: str
    departure_date: str
    stops: int
    similarity_score: Optional[float]

class RecommendationResponse(BaseModel):
    places: List[PlaceResponse]
    flights: List[FlightResponse]
    total_cost: Optional[float]
    itinerary_suggestions: List[str]

class DestinationResponse(BaseModel):
    id: str
    name: str
    country: str
    kind: str
    cost_day_usd: float
    description: str
    image_url: Optional[str]
    total_cost_estimate: float
    similarity_score: Optional[float]

class DestinationDetailsResponse(BaseModel):
    destination: Dict[str, Any]
    transport_options: List[Dict[str, Any]]
    accommodations: List[Dict[str, Any]]
    activities: List[Dict[str, Any]]

# Dependency to check if Supabase is available
def get_supabase():
    if supabase_loader is None:
        raise HTTPException(status_code=503, detail="Database not configured")
    return supabase_loader

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Travel AI API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database_connected": supabase_loader is not None
    }

@app.post("/search/places", response_model=List[PlaceResponse])
async def search_places(
    request: PlaceSearchRequest,
    supabase: SupabaseLoader = Depends(get_supabase)
):
    """Search for places using semantic similarity."""
    try:
        logger.info(f"Searching places for query: {request.query}")
        
        # For now, we'll return mock data since we need to implement
        # the actual database query with vector similarity
        # In a real implementation, you would:
        # 1. Generate embedding for the query
        # 2. Query Supabase with vector similarity
        # 3. Return filtered results
        
        # Mock response for demonstration
        mock_places = [
            {
                "place_id": "eiffel_tower",
                "name": "Eiffel Tower",
                "type": "cultural",
                "categories": "cultural,historic,architecture",
                "latitude": 48.8584,
                "longitude": 2.2945,
                "country": "France",
                "city": "Paris",
                "rate": 8.5,
                "description": "Iconic iron lattice tower on the Champ de Mars in Paris",
                "image": "https://example.com/eiffel_tower.jpg",
                "similarity_score": 0.95
            },
            {
                "place_id": "louvre_museum",
                "name": "Louvre Museum",
                "type": "cultural",
                "categories": "cultural,museums,historic",
                "latitude": 48.8606,
                "longitude": 2.3376,
                "country": "France",
                "city": "Paris",
                "rate": 8.8,
                "description": "World's largest art museum and historic monument",
                "image": "https://example.com/louvre.jpg",
                "similarity_score": 0.87
            }
        ]
        
        # Filter by rating if specified
        if request.min_rating > 0:
            mock_places = [p for p in mock_places if p["rate"] >= request.min_rating]
        
        # Limit results
        mock_places = mock_places[:request.limit]
        
        return mock_places
        
    except Exception as e:
        logger.error(f"Error searching places: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/search/flights", response_model=List[FlightResponse])
async def search_flights(
    request: FlightSearchRequest,
    supabase: SupabaseLoader = Depends(get_supabase)
):
    """Search for flights."""
    try:
        logger.info(f"Searching flights: {request.origin} to {request.destination}")
        
        # Mock response for demonstration
        mock_flights = [
            {
                "quote_id": "flight_001",
                "min_price": 450.0,
                "currency": "USD",
                "direct": True,
                "origin_id": request.origin,
                "destination_id": request.destination,
                "departure_date": request.departure_date,
                "stops": 0,
                "similarity_score": 0.92
            },
            {
                "quote_id": "flight_002",
                "min_price": 380.0,
                "currency": "USD",
                "direct": False,
                "origin_id": request.origin,
                "destination_id": request.destination,
                "departure_date": request.departure_date,
                "stops": 1,
                "similarity_score": 0.85
            }
        ]
        
        return mock_flights
        
    except Exception as e:
        logger.error(f"Error searching flights: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/recommendations", response_model=RecommendationResponse)
async def get_travel_recommendations(
    request: TravelRecommendationRequest,
    supabase: SupabaseLoader = Depends(get_supabase)
):
    """Get AI-powered travel recommendations."""
    try:
        logger.info(f"Generating recommendations for: {request.user_preferences}")
        
        # Mock response for demonstration
        # In a real implementation, you would:
        # 1. Analyze user preferences
        # 2. Generate embeddings for the preferences
        # 3. Find similar places and flights
        # 4. Create personalized recommendations
        
        mock_recommendations = {
            "places": [
                {
                    "place_id": "sagrada_familia",
                    "name": "Sagrada Familia",
                    "type": "cultural",
                    "categories": "cultural,religious,architecture",
                    "latitude": 41.4036,
                    "longitude": 2.1744,
                    "country": "Spain",
                    "city": "Barcelona",
                    "rate": 9.2,
                    "description": "Famous unfinished church designed by Antoni Gaudí",
                    "image": "https://example.com/sagrada_familia.jpg",
                    "similarity_score": 0.88
                }
            ],
            "flights": [
                {
                    "quote_id": "rec_flight_001",
                    "min_price": 520.0,
                    "currency": "USD",
                    "direct": True,
                    "origin_id": "JFK-sky",
                    "destination_id": "BCN-sky",
                    "departure_date": "2024-06-15",
                    "stops": 0,
                    "similarity_score": 0.91
                }
            ],
            "total_cost": 1040.0,
            "itinerary_suggestions": [
                "Visit Sagrada Familia in the morning to avoid crowds",
                "Explore the Gothic Quarter in the afternoon",
                "Enjoy tapas in the evening"
            ]
        }
        
        return mock_recommendations
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/places/popular")
async def get_popular_places(
    limit: int = Query(10, ge=1, le=50),
    supabase: SupabaseLoader = Depends(get_supabase)
):
    """Get popular places based on ratings."""
    try:
        # Mock response for demonstration
        popular_places = [
            {
                "place_id": "eiffel_tower",
                "name": "Eiffel Tower",
                "type": "cultural",
                "categories": "cultural,historic,architecture",
                "latitude": 48.8584,
                "longitude": 2.2945,
                "country": "France",
                "city": "Paris",
                "rate": 8.5,
                "description": "Iconic iron lattice tower on the Champ de Mars in Paris",
                "image": "https://example.com/eiffel_tower.jpg"
            },
            {
                "place_id": "colosseum",
                "name": "Colosseum",
                "type": "historic",
                "categories": "historic,cultural,architecture",
                "latitude": 41.8902,
                "longitude": 12.4922,
                "country": "Italy",
                "city": "Rome",
                "rate": 8.7,
                "description": "Ancient amphitheater in the center of Rome",
                "image": "https://example.com/colosseum.jpg"
            }
        ]
        
        return popular_places[:limit]
        
    except Exception as e:
        logger.error(f"Error getting popular places: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/flights/trending")
async def get_trending_flights(
    limit: int = Query(10, ge=1, le=50),
    supabase: SupabaseLoader = Depends(get_supabase)
):
    """Get trending flight routes."""
    try:
        # Mock response for demonstration
        trending_flights = [
            {
                "route": "JFK-LAX",
                "avg_price": 420.0,
                "currency": "USD",
                "popularity_score": 0.95,
                "description": "New York to Los Angeles"
            },
            {
                "route": "LHR-CDG",
                "avg_price": 180.0,
                "currency": "EUR",
                "popularity_score": 0.88,
                "description": "London to Paris"
            }
        ]
        
        return trending_flights[:limit]
        
    except Exception as e:
        logger.error(f"Error getting trending flights: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/places/{place_id}")
async def get_place_details(
    place_id: str,
    supabase: SupabaseLoader = Depends(get_supabase)
):
    """Get detailed information about a specific place."""
    try:
        # Mock response for demonstration
        place_details = {
            "place_id": place_id,
            "name": "Sample Place",
            "description": "Detailed information about this place",
            "images": ["https://example.com/image1.jpg"],
            "reviews": [],
            "similar_places": []
        }
        
        return place_details
        
    except Exception as e:
        logger.error(f"Error getting place details: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/recommend", response_model=List[DestinationResponse])
async def recommend_destinations(
    type: Optional[str] = Query(None, description="Destination type (beach, mountain, city, etc.)"),
    budget: Optional[float] = Query(None, description="Maximum budget in USD"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    stay_type: Optional[str] = Query(None, description="Accommodation type (hotel, airbnb, resort)"),
    activities: Optional[str] = Query(None, description="Comma-separated list of activities"),
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),
    supabase: SupabaseLoader = Depends(get_supabase)
):
    """Get destination recommendations based on user preferences."""
    try:
        logger.info(f"Getting recommendations: type={type}, budget={budget}, stay_type={stay_type}")
        
        # Calculate trip duration if dates provided
        trip_duration = 7  # default
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                trip_duration = (end - start).days
            except ValueError:
                logger.warning("Invalid date format, using default duration")
        
        # Adjust budget for trip duration
        adjusted_budget = budget
        if budget and trip_duration > 0:
            adjusted_budget = budget / trip_duration
        
        # Build query for destinations
        query = supabase.table('destinations').select('*')
        
        # Apply filters
        if type:
            query = query.eq('kind', type)
        
        if adjusted_budget:
            query = query.lte('cost_day_usd', adjusted_budget)
        
        # Execute query
        result = query.limit(limit).execute()
        
        if not result.data:
            # Return mock data if no results
            mock_destinations = [
                {
                    "id": "bali-id",
                    "name": "Bali",
                    "country": "Indonesia",
                    "kind": "beach" if type == "beach" else "island",
                    "cost_day_usd": 120.0,
                    "description": "Tropical paradise with beautiful beaches and rich culture",
                    "image_url": "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=800&h=600&fit=crop",
                    "total_cost_estimate": 840.0,
                    "similarity_score": 0.95
                },
                {
                    "id": "cancun-id",
                    "name": "Cancun",
                    "country": "Mexico",
                    "kind": "beach" if type == "beach" else "city",
                    "cost_day_usd": 150.0,
                    "description": "Famous beach destination with crystal clear waters",
                    "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&h=600&fit=crop",
                    "total_cost_estimate": 1050.0,
                    "similarity_score": 0.92
                },
                {
                    "id": "oahu-id",
                    "name": "Oahu",
                    "country": "USA",
                    "kind": "beach" if type == "beach" else "island",
                    "cost_day_usd": 200.0,
                    "description": "Hawaiian island with stunning beaches and surf culture",
                    "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop",
                    "total_cost_estimate": 1400.0,
                    "similarity_score": 0.88
                }
            ]
            
            # Filter by type if specified
            if type:
                mock_destinations = [d for d in mock_destinations if d["kind"] == type]
            
            # Filter by budget if specified
            if budget:
                mock_destinations = [d for d in mock_destinations if d["total_cost_estimate"] <= budget]
            
            return mock_destinations[:limit]
        
        # Process real results
        destinations = []
        for dest in result.data:
            destinations.append({
                "id": dest["id"],
                "name": dest["name"],
                "country": dest["country"],
                "kind": dest["kind"],
                "cost_day_usd": dest["cost_day_usd"],
                "description": dest["description"],
                "image_url": dest["image_url"],
                "total_cost_estimate": dest["cost_day_usd"] * trip_duration,
                "similarity_score": 0.85  # Placeholder
            })
        
        return destinations
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/details/{destination_id}", response_model=DestinationDetailsResponse)
async def get_destination_details(
    destination_id: str,
    supabase: SupabaseLoader = Depends(get_supabase)
):
    """Get detailed information about a destination including costs and activities."""
    try:
        logger.info(f"Getting details for destination: {destination_id}")
        
        # Try to get real data first
        try:
            # Get destination details
            dest_result = supabase.table('destinations').select('*').eq('id', destination_id).execute()
            
            if dest_result.data:
                dest = dest_result.data[0]
                
                # Get transport options
                transport_result = supabase.table('transport_options').select('*').eq('dest_id', destination_id).execute()
                transport_options = transport_result.data if transport_result.data else []
                
                # Get accommodations
                acc_result = supabase.table('accommodations').select('*').eq('dest_id', destination_id).execute()
                accommodations = acc_result.data if acc_result.data else []
                
                # Get activities
                act_result = supabase.table('activities').select('*').eq('dest_id', destination_id).execute()
                activities = act_result.data if act_result.data else []
                
                return {
                    "destination": dest,
                    "transport_options": transport_options,
                    "accommodations": accommodations,
                    "activities": activities
                }
        except Exception as e:
            logger.warning(f"Could not fetch real data: {e}")
        
        # Return mock data if real data not available
        mock_details = {
            "destination": {
                "id": destination_id,
                "name": "Bali",
                "country": "Indonesia",
                "kind": "beach",
                "cost_day_usd": 120.0,
                "description": "Tropical paradise with beautiful beaches and rich culture",
                "image_url": "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=800&h=600&fit=crop",
                "latitude": -8.3405,
                "longitude": 115.0920,
                "season_high": "summer"
            },
            "transport_options": [
                {
                    "id": "transport-1",
                    "mode": "flight",
                    "avg_price_usd": 450.0,
                    "duration_hours": 8,
                    "description": "International flight to Bali"
                },
                {
                    "id": "transport-2",
                    "mode": "car",
                    "avg_price_usd": 25.0,
                    "duration_hours": 1,
                    "description": "Local car rental"
                }
            ],
            "accommodations": [
                {
                    "id": "acc-1",
                    "type": "resort",
                    "avg_price_usd": 150.0,
                    "rating": 4.5,
                    "description": "Luxury beachfront resort",
                    "amenities": ["pool", "spa", "restaurant", "gym"]
                },
                {
                    "id": "acc-2",
                    "type": "airbnb",
                    "avg_price_usd": 80.0,
                    "rating": 4.2,
                    "description": "Local villa with private pool",
                    "amenities": ["kitchen", "wifi", "pool"]
                }
            ],
            "activities": [
                {
                    "id": "act-1",
                    "title": "Surfing Lessons",
                    "category": "water_sports",
                    "description": "Learn to surf on Bali's famous waves",
                    "avg_price_usd": 45.0,
                    "duration_hours": 3,
                    "difficulty": "moderate"
                },
                {
                    "id": "act-2",
                    "title": "Temple Tour",
                    "category": "cultural",
                    "description": "Visit ancient temples and learn about Balinese culture",
                    "avg_price_usd": 35.0,
                    "duration_hours": 4,
                    "difficulty": "easy"
                },
                {
                    "id": "act-3",
                    "title": "Rice Terrace Hiking",
                    "category": "outdoor",
                    "description": "Hike through beautiful rice terraces",
                    "avg_price_usd": 25.0,
                    "duration_hours": 2,
                    "difficulty": "easy"
                }
            ]
        }
        
        return mock_details
        
    except Exception as e:
        logger.error(f"Error getting destination details: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/flight-deal")
async def get_flight_deal(
    to: str = Query(..., description="Destination airport code"),
    from_: str = Query(..., alias="from", description="Origin airport code"),
    supabase: SupabaseLoader = Depends(get_supabase)
):
    """Get cheapest flight estimate (optional Amadeus integration)."""
    try:
        logger.info(f"Getting flight deal: {from_} to {to}")
        
        # Mock flight deal response
        # In a real implementation, you'd integrate with Amadeus API
        base_price = random.uniform(300, 800)
        discount_percentage = random.uniform(5, 25)
        discounted_price = base_price * (1 - discount_percentage / 100)
        
        return {
            "origin": from_,
            "destination": to,
            "base_price_usd": round(base_price, 2),
            "discounted_price_usd": round(discounted_price, 2),
            "discount_percentage": round(discount_percentage, 1),
            "deal_message": f"💸 {round(discount_percentage, 1)}% off typical price!",
            "airline": random.choice(["American Airlines", "Delta", "United", "Southwest"]),
            "duration_hours": random.randint(2, 8),
            "stops": random.choice([0, 1, 2])
        }
        
    except Exception as e:
        logger.error(f"Error getting flight deal: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 