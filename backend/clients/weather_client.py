"""
Weather client using WeatherAPI.com.
"""

import httpx
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class WeatherClient:
    """Client for weather data using WeatherAPI.com."""
    
    def __init__(self):
        self.base_url = settings.WEATHER_BASE_URL
        self.api_key = settings.WEATHER_API_KEY
    
    async def get_current_weather(self, location: str) -> Optional[Dict]:
        """Get current weather for a location."""
        try:
            if not self.api_key:
                logger.warning("Weather API key not configured, using mock data")
                return self._get_mock_current_weather(location)
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"{self.base_url}/current.json"
                params = {
                    "key": self.api_key,
                    "q": location,
                    "aqi": "no"
                }
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                weather_data = {
                    "location": {
                        "name": data["location"]["name"],
                        "country": data["location"]["country"],
                        "lat": data["location"]["lat"],
                        "lon": data["location"]["lon"]
                    },
                    "current": {
                        "temperature": f"{data['current']['temp_c']}°C",
                        "condition": data["current"]["condition"]["text"],
                        "humidity": f"{data['current']['humidity']}%",
                        "wind_speed": f"{data['current']['wind_kph']} km/h",
                        "feels_like": f"{data['current']['feelslike_c']}°C"
                    }
                }
                
                logger.info(f"Retrieved current weather for {location}")
                return weather_data
                
        except httpx.RequestError as e:
            logger.error(f"Error fetching current weather: {e}")
            return self._get_mock_current_weather(location)
        except Exception as e:
            logger.error(f"Unexpected error in get_current_weather: {e}")
            return self._get_mock_current_weather(location)
    
    async def get_forecast(self, location: str, days: int = 3) -> Optional[Dict]:
        """Get weather forecast for a location."""
        try:
            if not self.api_key:
                logger.warning("Weather API key not configured, using mock data")
                return self._get_mock_forecast(location, days)
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"{self.base_url}/forecast.json"
                params = {
                    "key": self.api_key,
                    "q": location,
                    "days": days,
                    "aqi": "no",
                    "alerts": "no"
                }
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                forecast_data = {
                    "location": {
                        "name": data["location"]["name"],
                        "country": data["location"]["country"]
                    },
                    "current": {
                        "temperature": f"{data['current']['temp_c']}°C",
                        "condition": data["current"]["condition"]["text"],
                        "humidity": f"{data['current']['humidity']}%"
                    },
                    "forecast": []
                }
                
                for day in data["forecast"]["forecastday"]:
                    forecast_data["forecast"].append({
                        "date": day["date"],
                        "day": self._get_day_name(day["date"]),
                        "temp": f"{day['day']['avgtemp_c']}°C",
                        "condition": day["day"]["condition"]["text"],
                        "max_temp": f"{day['day']['maxtemp_c']}°C",
                        "min_temp": f"{day['day']['mintemp_c']}°C",
                        "chance_of_rain": f"{day['day']['daily_chance_of_rain']}%"
                    })
                
                logger.info(f"Retrieved {days}-day forecast for {location}")
                return forecast_data
                
        except httpx.RequestError as e:
            logger.error(f"Error fetching forecast: {e}")
            return self._get_mock_forecast(location, days)
        except Exception as e:
            logger.error(f"Unexpected error in get_forecast: {e}")
            return self._get_mock_forecast(location, days)
    
    async def get_weather_summary(self, location: str) -> Optional[Dict]:
        """Get a comprehensive weather summary including current and forecast."""
        try:
            current = await self.get_current_weather(location)
            forecast = await self.get_forecast(location, 3)
            
            if current and forecast:
                return {
                    "location": current["location"],
                    "current": current["current"],
                    "forecast": forecast["forecast"]
                }
            elif current:
                return current
            elif forecast:
                return forecast
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting weather summary: {e}")
            return self._get_mock_weather_summary(location)
    
    def _get_day_name(self, date_str: str) -> str:
        """Convert date string to day name."""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%A")
        except:
            return "Unknown"
    
    def _get_mock_current_weather(self, location: str) -> Dict:
        """Mock current weather data."""
        return {
            "location": {
                "name": location,
                "country": "Unknown",
                "lat": 0.0,
                "lon": 0.0
            },
            "current": {
                "temperature": "22°C",
                "condition": "Sunny",
                "humidity": "65%",
                "wind_speed": "10 km/h",
                "feels_like": "24°C"
            }
        }
    
    def _get_mock_forecast(self, location: str, days: int) -> Dict:
        """Mock forecast data."""
        forecast = []
        for i in range(days):
            day_names = ["Today", "Tomorrow", "Day 3", "Day 4", "Day 5"]
            conditions = ["Sunny", "Partly Cloudy", "Light Rain", "Cloudy"]
            
            forecast.append({
                "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "day": day_names[i] if i < len(day_names) else f"Day {i+1}",
                "temp": f"{20 + i}°C",
                "condition": conditions[i % len(conditions)],
                "max_temp": f"{25 + i}°C",
                "min_temp": f"{15 + i}°C",
                "chance_of_rain": f"{10 + i * 5}%"
            })
        
        return {
            "location": {
                "name": location,
                "country": "Unknown"
            },
            "current": {
                "temperature": "22°C",
                "condition": "Sunny",
                "humidity": "65%"
            },
            "forecast": forecast
        }
    
    def _get_mock_weather_summary(self, location: str) -> Dict:
        """Mock weather summary data."""
        return {
            "location": {
                "name": location,
                "country": "Unknown"
            },
            "current": {
                "temperature": "22°C",
                "condition": "Sunny",
                "humidity": "65%"
            },
            "forecast": [
                {
                    "day": "Today",
                    "temp": "22°C",
                    "condition": "Sunny"
                },
                {
                    "day": "Tomorrow",
                    "temp": "24°C",
                    "condition": "Partly Cloudy"
                },
                {
                    "day": "Day 3",
                    "temp": "21°C",
                    "condition": "Light Rain"
                }
            ]
        }

# Global weather client instance
weather_client = WeatherClient() 