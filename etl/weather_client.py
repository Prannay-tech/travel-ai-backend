import os
from dotenv import load_dotenv
load_dotenv()
import requests
from datetime import datetime, timedelta

class WeatherClient:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1"
        
    def get_current_weather(self, lat, lon):
        """Get current weather for a location"""
        url = f"{self.base_url}/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
            "timezone": "auto"
        }
        print("Requesting weather:", url)
        print("Params:", params)
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_forecast(self, lat, lon, days=7):
        """Get weather forecast for a location"""
        url = f"{self.base_url}/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,weather_code",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
            "timezone": "auto",
            "forecast_days": days
        }
        print("Requesting forecast:", url)
        print("Params:", params)
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_historical_weather(self, lat, lon, start_date, end_date):
        """Get historical weather data"""
        url = f"{self.base_url}/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation,weather_code",
            "start_date": start_date,
            "end_date": end_date,
            "timezone": "auto"
        }
        print("Requesting historical weather:", url)
        print("Params:", params)
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json() 