"""
Weather API Integration
Supports multiple weather providers for destination weather data.
"""

import httpx
import os
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# API Keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

class WeatherAPI:
    """Weather data provider using WeatherAPI.com"""
    
    def __init__(self):
        self.api_key = WEATHER_API_KEY
        self.base_url = "http://api.weatherapi.com/v1"
        self.available = bool(self.api_key)
        
    async def get_current_weather(self, location: str) -> Optional[Dict]:
        """Get current weather for a location"""
        if not self.available:
            return self._get_mock_weather(location)
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/current.json",
                    params={
                        "key": self.api_key,
                        "q": location,
                        "aqi": "no"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_weather_data(data)
                else:
                    logger.error(f"Weather API error: {response.status_code}")
                    return self._get_mock_weather(location)
                    
        except Exception as e:
            logger.error(f"Error fetching weather: {e}")
            return self._get_mock_weather(location)
    
    async def get_forecast(self, location: str, days: int = 7) -> Optional[Dict]:
        """Get weather forecast for a location"""
        if not self.available:
            return self._get_mock_forecast(location, days)
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/forecast.json",
                    params={
                        "key": self.api_key,
                        "q": location,
                        "days": days,
                        "aqi": "no"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_forecast_data(data)
                else:
                    logger.error(f"Weather forecast API error: {response.status_code}")
                    return self._get_mock_forecast(location, days)
                    
        except Exception as e:
            logger.error(f"Error fetching weather forecast: {e}")
            return self._get_mock_forecast(location, days)
    
    def _parse_weather_data(self, data: Dict) -> Dict:
        """Parse weather API response"""
        try:
            current = data.get("current", {})
            location = data.get("location", {})
            
            return {
                "location": location.get("name", "Unknown"),
                "country": location.get("country", "Unknown"),
                "temperature_c": current.get("temp_c"),
                "temperature_f": current.get("temp_f"),
                "condition": current.get("condition", {}).get("text", "Unknown"),
                "condition_icon": current.get("condition", {}).get("icon", ""),
                "humidity": current.get("humidity"),
                "wind_kph": current.get("wind_kph"),
                "wind_mph": current.get("wind_mph"),
                "feels_like_c": current.get("feelslike_c"),
                "feels_like_f": current.get("feelslike_f"),
                "uv": current.get("uv"),
                "last_updated": current.get("last_updated"),
                "source": "WeatherAPI.com"
            }
        except Exception as e:
            logger.error(f"Error parsing weather data: {e}")
            return self._get_mock_weather("Unknown")
    
    def _parse_forecast_data(self, data: Dict) -> Dict:
        """Parse weather forecast API response"""
        try:
            location = data.get("location", {})
            forecast = data.get("forecast", {}).get("forecastday", [])
            
            forecast_data = []
            for day in forecast:
                day_data = day.get("day", {})
                forecast_data.append({
                    "date": day.get("date"),
                    "max_temp_c": day_data.get("maxtemp_c"),
                    "min_temp_c": day_data.get("mintemp_c"),
                    "max_temp_f": day_data.get("maxtemp_f"),
                    "min_temp_f": day_data.get("mintemp_f"),
                    "condition": day_data.get("condition", {}).get("text", "Unknown"),
                    "condition_icon": day_data.get("condition", {}).get("icon", ""),
                    "precipitation_mm": day_data.get("totalprecip_mm"),
                    "precipitation_in": day_data.get("totalprecip_in"),
                    "humidity": day_data.get("avghumidity"),
                    "uv": day_data.get("uv")
                })
            
            return {
                "location": location.get("name", "Unknown"),
                "country": location.get("country", "Unknown"),
                "forecast": forecast_data,
                "source": "WeatherAPI.com"
            }
        except Exception as e:
            logger.error(f"Error parsing forecast data: {e}")
            return self._get_mock_forecast("Unknown", 7)
    
    def _get_mock_weather(self, location: str) -> Dict:
        """Return mock weather data"""
        return {
            "location": location,
            "country": "Unknown",
            "temperature_c": 22,
            "temperature_f": 72,
            "condition": "Sunny",
            "condition_icon": "//cdn.weatherapi.com/weather/64x64/day/113.png",
            "humidity": 65,
            "wind_kph": 15,
            "wind_mph": 9,
            "feels_like_c": 24,
            "feels_like_f": 75,
            "uv": 5,
            "last_updated": datetime.now().isoformat(),
            "source": "Mock Data"
        }
    
    def _get_mock_forecast(self, location: str, days: int) -> Dict:
        """Return mock forecast data"""
        forecast_data = []
        for i in range(days):
            forecast_data.append({
                "date": (datetime.now().date() + timedelta(days=i)).isoformat(),
                "max_temp_c": 25 + i,
                "min_temp_c": 15 + i,
                "max_temp_f": 77 + i,
                "min_temp_f": 59 + i,
                "condition": "Sunny" if i % 2 == 0 else "Partly Cloudy",
                "condition_icon": "//cdn.weatherapi.com/weather/64x64/day/113.png",
                "precipitation_mm": 0,
                "precipitation_in": 0,
                "humidity": 65,
                "uv": 5
            })
        
        return {
            "location": location,
            "country": "Unknown",
            "forecast": forecast_data,
            "source": "Mock Data"
        }

# Global instance
weather_api = WeatherAPI()
