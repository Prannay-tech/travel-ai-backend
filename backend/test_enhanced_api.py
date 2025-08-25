"""
Test script for the enhanced Travel AI backend API.
"""

import asyncio
import httpx
import json
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8000"

async def test_health_check():
    """Test the health check endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print("Health Check:")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()

async def test_currency_conversion():
    """Test currency conversion."""
    async with httpx.AsyncClient() as client:
        # Test USD to EUR conversion
        data = {
            "amount": 1000.0,
            "from_currency": "USD",
            "to_currency": "EUR"
        }
        response = await client.post(f"{BASE_URL}/currency/convert", json=data)
        print("Currency Conversion (USD to EUR):")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()

async def test_exchange_rates():
    """Test exchange rates endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/currency/rates?base_currency=USD")
        print("Exchange Rates:")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()

async def test_weather_summary():
    """Test weather summary endpoint."""
    async with httpx.AsyncClient() as client:
        data = {
            "location": "Tokyo, Japan",
            "days": 3
        }
        response = await client.post(f"{BASE_URL}/weather/summary", json=data)
        print("Weather Summary (Tokyo):")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()

async def test_holidays():
    """Test holidays endpoint."""
    async with httpx.AsyncClient() as client:
        data = {
            "country": "USA",
            "year": 2024
        }
        response = await client.post(f"{BASE_URL}/holidays", json=data)
        print("Holidays (USA 2024):")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()

async def test_destination_search():
    """Test destination search."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/destinations/search",
            params={
                "travel_type": "international",
                "destination_type": "beach",
                "currency": "EUR"
            }
        )
        print("Destination Search (International Beach, EUR):")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()

async def test_enhanced_recommendations():
    """Test enhanced recommendations endpoint."""
    async with httpx.AsyncClient() as client:
        data = {
            "destination": "beach",
            "budget": "5000",
            "travelDates": "summer 2024",
            "currentLocation": "New York",
            "preferences": "family-friendly, relaxing",
            "currency": "EUR",
            "travelType": "international"
        }
        response = await client.post(f"{BASE_URL}/recommendations/enhanced", json=data)
        print("Enhanced Recommendations:")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()

async def test_domestic_destinations():
    """Test domestic destinations endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/destinations/domestic")
        print("Domestic Destinations:")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()

async def test_international_destinations():
    """Test international destinations endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/destinations/international")
        print("International Destinations:")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()

async def main():
    """Run all tests."""
    print("🧪 Testing Enhanced Travel AI Backend API")
    print("=" * 50)
    print(f"Base URL: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    try:
        # Test basic functionality
        await test_health_check()
        await test_currency_conversion()
        await test_exchange_rates()
        
        # Test data sources
        await test_weather_summary()
        await test_holidays()
        
        # Test destination data
        await test_domestic_destinations()
        await test_international_destinations()
        await test_destination_search()
        
        # Test main recommendation endpoint
        await test_enhanced_recommendations()
        
        print("✅ All tests completed successfully!")
        
    except httpx.ConnectError:
        print("❌ Could not connect to the server. Make sure the backend is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 