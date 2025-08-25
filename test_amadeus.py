#!/usr/bin/env python3
"""
Simple test script for Amadeus API integration.
"""

import os
import sys
from datetime import datetime, timedelta

# Add the etl directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'etl'))

from fetch_amadeus import AmadeusFetcher

def test_amadeus_integration():
    """Test the Amadeus API integration."""
    print("🧪 Testing Amadeus API Integration")
    print("=" * 50)
    
    # Initialize fetcher with the provided API key
    api_key = "8W8ZGIcN61pNWmljxuc350cSGFUGXTCv"
    fetcher = AmadeusFetcher(api_key)
    
    try:
        # Test 1: Airport autocomplete
        print("\n1. Testing airport autocomplete...")
        airports = fetcher.get_airport_autocomplete("New York")
        
        if airports:
            print(f"✅ Found {len(airports)} airports/cities for 'New York'")
            for airport in airports[:3]:
                name = airport.get('name', 'N/A')
                code = airport.get('iataCode', 'N/A')
                print(f"   - {name} ({code})")
        else:
            print("❌ No airports found")
            print("   This might be due to missing client secret or API limits")
        
        # Test 2: Flight search (limited to avoid rate limits)
        print("\n2. Testing flight search...")
        departure_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        flights = fetcher.search_flights("JFK", "LAX", departure_date, max_price=1000)
        
        if flights.get('data'):
            print(f"✅ Found {len(flights['data'])} flights from JFK to LAX")
            
            # Show sample flight data
            for i, flight in enumerate(flights['data'][:2]):
                print(f"   Flight {i+1}:")
                price = flight.get('price', {}).get('total', 'N/A')
                print(f"     Price: ${price}")
                
                itineraries = flight.get('itineraries', [])
                if itineraries:
                    segments = itineraries[0].get('segments', [])
                    stops = max(0, len(segments) - 1)
                    duration = itineraries[0].get('duration', 'N/A')
                    print(f"     Stops: {stops}")
                    print(f"     Duration: {duration}")
        else:
            print("❌ No flights found")
            print("   This might be due to missing client secret or API limits")
        
        print("\n📝 Important Notes:")
        print("   1. You need to get your client secret from Amadeus developer portal")
        print("   2. Update the client_secret in fetch_amadeus.py")
        print("   3. The test API has limited functionality")
        print("   4. Consider upgrading to production API for full features")
        
        print("\n🎉 Amadeus API integration test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    test_amadeus_integration() 