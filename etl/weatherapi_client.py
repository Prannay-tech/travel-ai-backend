import os
from dotenv import load_dotenv
load_dotenv()
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional

class WeatherAPIClient:
    def __init__(self):
        self.api_key = os.getenv("WEATHERAPI_KEY") or "0199245a95814f5a968202129251607"
        self.base_url = "http://api.weatherapi.com/v1"
        
    def get_current_weather(self, lat: float, lon: float) -> Dict:
        """Get current weather for a location using coordinates"""
        url = f"{self.base_url}/current.json"
        params = {
            "key": self.api_key,
            "q": f"{lat},{lon}",
            "aqi": "no"  # Air quality data
        }
        
        print(f"Requesting current weather: {url}")
        print(f"Params: {params}")
        
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_forecast(self, lat: float, lon: float, days: int = 7) -> Dict:
        """Get weather forecast for a location"""
        url = f"{self.base_url}/forecast.json"
        params = {
            "key": self.api_key,
            "q": f"{lat},{lon}",
            "days": days,
            "aqi": "no",
            "alerts": "no"
        }
        
        print(f"Requesting forecast: {url}")
        print(f"Params: {params}")
        
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_historical_weather(self, lat: float, lon: float, date: str) -> Dict:
        """Get historical weather data for a specific date"""
        url = f"{self.base_url}/history.json"
        params = {
            "key": self.api_key,
            "q": f"{lat},{lon}",
            "dt": date,
            "aqi": "no"
        }
        
        print(f"Requesting historical weather: {url}")
        print(f"Params: {params}")
        
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_weather_by_city(self, city: str) -> Dict:
        """Get current weather for a city by name"""
        url = f"{self.base_url}/current.json"
        params = {
            "key": self.api_key,
            "q": city,
            "aqi": "no"
        }
        
        print(f"Requesting weather for city: {url}")
        print(f"Params: {params}")
        
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_astronomy(self, lat: float, lon: float, date: Optional[str] = None) -> Dict:
        """Get astronomy data (sunrise, sunset, moonrise, moonset)"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        url = f"{self.base_url}/astronomy.json"
        params = {
            "key": self.api_key,
            "q": f"{lat},{lon}",
            "dt": date
        }
        
        print(f"Requesting astronomy data: {url}")
        print(f"Params: {params}")
        
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json() 