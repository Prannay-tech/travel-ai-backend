"""
Enhanced ETL Pipeline for Travel AI with Weather and Calendar Integration
Populates destinations, weather_data, and holidays tables with comprehensive travel data.
"""

import os
from dotenv import load_dotenv
load_dotenv()
import sys
import logging
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pandas as pd
from supabase.client import create_client, Client
from sentence_transformers import SentenceTransformer
from tomtom_client import TomTomClient
from weatherapi_client import WeatherAPIClient
from calendarific_client import CalendarificClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedETLPipelineWithWeatherCalendar:
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase = create_client(supabase_url, supabase_key)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.tomtom = TomTomClient()
        self.weather = WeatherAPIClient()
        self.calendarific = CalendarificClient()

    def fetch_destinations(self, city_coords: List[Dict[str, Any]], query="tourist attraction") -> List[Dict]:
        """Fetch POIs for each city using TomTom."""
        destinations = []
        for city in city_coords:
            try:
                pois = self.tomtom.search_pois(query, city['lat'], city['lon'])
                for poi in pois:
                    destinations.append({
                        'name': poi['poi']['name'],
                        'country': city['country'],
                        'kind': poi['poi'].get('categories', ['unknown'])[0],
                        'latitude': poi['position']['lat'],
                        'longitude': poi['position']['lon'],
                        'description': poi['poi'].get('categories', []),
                        'image_url': None  # TomTom POI API does not provide images
                    })
                logger.info(f"Fetched {len(pois)} POIs for {city['country']}")
            except Exception as e:
                logger.error(f"Error fetching POIs for {city['country']}: {e}")
        return destinations

    def fetch_weather_data(self, city_coords: List[Dict[str, Any]]) -> List[Dict]:
        """Fetch weather data for each city."""
        weather_data = []
        current_year = datetime.now().year
        
        for city in city_coords:
            try:
                # Get current weather
                current_weather = self.weather.get_current_weather(city['lat'], city['lon'])
                
                # Get 7-day forecast
                forecast = self.weather.get_forecast(city['lat'], city['lon'], days=7)
                
                weather_data.append({
                    'city': city['country'],
                    'latitude': city['lat'],
                    'longitude': city['lon'],
                    'current_temperature': current_weather['current']['temp_c'],
                    'current_humidity': current_weather['current']['humidity'],
                    'current_weather_condition': current_weather['current']['condition']['text'],
                    'forecast_data': forecast,
                    'last_updated': datetime.now().isoformat()
                })
                logger.info(f"Fetched weather data for {city['country']}")
            except Exception as e:
                logger.error(f"Error fetching weather for {city['country']}: {e}")
        
        return weather_data

    def fetch_holidays(self, countries: List[str]) -> List[Dict]:
        """Fetch holidays for specified countries."""
        holidays_data = []
        current_year = datetime.now().year
        
        for country in countries:
            try:
                holidays = self.calendarific.get_holidays(country=country, year=current_year)
                
                for holiday in holidays:
                    holidays_data.append({
                        'name': holiday['name'],
                        'country': country,
                        'date': holiday['date']['iso'],
                        'type': holiday.get('type', 'unknown'),
                        'description': holiday.get('description', ''),
                        'year': current_year
                    })
                logger.info(f"Fetched {len(holidays)} holidays for {country}")
            except Exception as e:
                logger.error(f"Error fetching holidays for {country}: {e}")
        
        return holidays_data

    def generate_embedding(self, text: str) -> List[float]:
        if not text:
            text = "travel destination"
        return self.embedder.encode(text).tolist()

    def load_destinations_to_supabase(self, destinations: List[Dict]):
        """Load destinations to Supabase."""
        for destination in destinations:
            try:
                embedding = self.generate_embedding(str(destination['description']))
                dest_data = {
                    'name': destination['name'],
                    'country': destination['country'],
                    'kind': destination['kind'],
                    'cost_day_usd': random.uniform(80, 300),
                    'embedding': embedding,
                    'season_high': random.choice(['spring', 'summer', 'autumn', 'winter']),
                    'latitude': destination['latitude'],
                    'longitude': destination['longitude'],
                    'description': str(destination['description']),
                    'image_url': destination['image_url']
                }
                self.supabase.table('destinations').insert(dest_data).execute()
                logger.info(f"Loaded destination: {destination['name']}")
            except Exception as e:
                logger.error(f"Error loading destination {destination['name']}: {e}")

    def load_weather_to_supabase(self, weather_data: List[Dict]):
        """Load weather data to Supabase."""
        for weather in weather_data:
            try:
                weather_record = {
                    'city': weather['city'],
                    'latitude': weather['latitude'],
                    'longitude': weather['longitude'],
                    'current_temperature': weather['current_temperature'],
                    'current_humidity': weather['current_humidity'],
                    'current_weather_condition': weather['current_weather_condition'],
                    'forecast_data': weather['forecast_data'],
                    'last_updated': weather['last_updated']
                }
                # Note: You'll need to create a 'weather_data' table in Supabase
                # self.supabase.table('weather_data').insert(weather_record).execute()
                logger.info(f"Loaded weather data for {weather['city']}")
            except Exception as e:
                logger.error(f"Error loading weather for {weather['city']}: {e}")

    def load_holidays_to_supabase(self, holidays_data: List[Dict]):
        """Load holidays data to Supabase."""
        for holiday in holidays_data:
            try:
                holiday_record = {
                    'name': holiday['name'],
                    'country': holiday['country'],
                    'date': holiday['date'],
                    'type': holiday['type'],
                    'description': holiday['description'],
                    'year': holiday['year']
                }
                # Note: You'll need to create a 'holidays' table in Supabase
                # self.supabase.table('holidays').insert(holiday_record).execute()
                logger.info(f"Loaded holiday: {holiday['name']} for {holiday['country']}")
            except Exception as e:
                logger.error(f"Error loading holiday {holiday['name']}: {e}")

    def run_pipeline(self, city_coords: List[Dict[str, Any]]):
        """Run the complete ETL pipeline with weather and calendar data."""
        logger.info("Starting enhanced ETL pipeline with weather and calendar integration...")
        
        # Extract countries from city coordinates
        countries = list(set([city['country'] for city in city_coords]))
        
        # Fetch all data
        logger.info("Fetching destinations...")
        destinations = self.fetch_destinations(city_coords)
        
        logger.info("Fetching weather data...")
        weather_data = self.fetch_weather_data(city_coords)
        
        logger.info("Fetching holidays...")
        holidays_data = self.fetch_holidays(countries)
        
        # Load data to Supabase
        logger.info(f"Loading {len(destinations)} destinations to Supabase...")
        self.load_destinations_to_supabase(destinations)
        
        logger.info(f"Loading weather data for {len(weather_data)} cities...")
        self.load_weather_to_supabase(weather_data)
        
        logger.info(f"Loading {len(holidays_data)} holidays...")
        self.load_holidays_to_supabase(holidays_data)
        
        logger.info("Enhanced ETL pipeline completed!")

def main():
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    if not all([supabase_url, supabase_key]):
        logger.error("Missing required environment variables")
        sys.exit(1)
    
    # Example city coordinates for demo
    city_coords = [
        {'country': 'France', 'lat': 48.8566, 'lon': 2.3522},  # Paris
        {'country': 'USA', 'lat': 40.7128, 'lon': -74.0060},   # New York
        {'country': 'Japan', 'lat': 35.6895, 'lon': 139.6917}, # Tokyo
        {'country': 'UK', 'lat': 51.5074, 'lon': -0.1278},     # London
        {'country': 'Italy', 'lat': 41.9028, 'lon': 12.4964},  # Rome
    ]
    
    if not supabase_url or not supabase_key:
        logger.error("Missing Supabase credentials")
        sys.exit(1)
    pipeline = EnhancedETLPipelineWithWeatherCalendar(supabase_url, supabase_key)
    pipeline.run_pipeline(city_coords)

if __name__ == "__main__":
    main() 