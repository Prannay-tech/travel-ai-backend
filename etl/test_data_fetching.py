#!/usr/bin/env python3
"""
Test script to fetch data from all APIs without loading to Supabase.
This helps verify that the data fetching components work correctly.
"""

import os
import sys
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

def test_data_fetching():
    """Test fetching data from all APIs."""
    try:
        from tomtom_client import TomTomClient
        from weather_client import WeatherClient
        from calendarific_client import CalendarificClient
        
        print("🔧 Initializing API clients...")
        tomtom = TomTomClient()
        weather = WeatherClient()
        calendarific = CalendarificClient()
        
        # Test city coordinates
        city_coords = [
            {'country': 'USA', 'lat': 40.7128, 'lon': -74.0060, 'name': 'New York'},
            {'country': 'France', 'lat': 48.8566, 'lon': 2.3522, 'name': 'Paris'},
        ]
        
        print("\n📍 Testing TomTom POI API...")
        for city in city_coords:
            try:
                pois = tomtom.search_pois("tourist attraction", city['lat'], city['lon'], limit=5)
                print(f"✅ Fetched {len(pois)} POIs for {city['name']}")
                if pois:
                    print(f"   Sample POI: {pois[0]['poi']['name']}")
            except Exception as e:
                print(f"❌ Error fetching POIs for {city['name']}: {e}")
        
        print("\n🌤️ Testing Weather API...")
        for city in city_coords:
            try:
                current_weather = weather.get_current_weather(city['lat'], city['lon'])
                print(f"✅ Fetched weather for {city['name']}: {current_weather['current']['temperature_2m']}°C")
            except Exception as e:
                print(f"❌ Error fetching weather for {city['name']}: {e}")
        
        print("\n📅 Testing Calendarific API...")
        countries = ['US', 'FR']  # USA and France
        for country in countries:
            try:
                holidays = calendarific.get_holidays(country=country, year=2024)
                print(f"✅ Fetched {len(holidays)} holidays for {country}")
                if holidays:
                    print(f"   Sample holiday: {holidays[0]['name']} on {holidays[0]['date']['iso']}")
            except Exception as e:
                print(f"❌ Error fetching holidays for {country}: {e}")
        
        print("\n✅ All API tests completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all required packages are installed")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_data_fetching()
    sys.exit(0 if success else 1) 