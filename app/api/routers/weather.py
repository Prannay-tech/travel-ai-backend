from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.services.weather_api import weather_api
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/{location}", response_model=Dict[str, Any])
async def get_current_weather(location: str):
    """Get current weather for a specific destination."""
    try:
        weather_data = await weather_api.get_current_weather(location)
        if not weather_data:
            raise HTTPException(status_code=404, detail="Weather data not found")
        return weather_data
    except Exception as e:
        logger.error(f"Error serving weather endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error fetching weather")

@router.get("/{location}/forecast", response_model=Dict[str, Any])
async def get_weather_forecast(location: str, days: int = 3):
    """Get weather forecast for a specific destination."""
    try:
        forecast_data = await weather_api.get_forecast(location, days)
        if not forecast_data:
            raise HTTPException(status_code=404, detail="Weather forecast not found")
        return forecast_data
    except Exception as e:
        logger.error(f"Error serving forecast endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error fetching forecast")
