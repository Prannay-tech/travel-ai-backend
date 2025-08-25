"""
Amadeus API integration for flight data fetching.
Amadeus provides comprehensive flight search and booking data.
"""

import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AmadeusFetcher:
    def __init__(self, api_key: str = "8W8ZGIcN61pNWmljxuc350cSGFUGXTCv"):
        self.api_key = api_key
        self.base_url = "https://test.api.amadeus.com/v2"  # Using test API for free tier
        self.access_token = None
        self.token_expiry = None
        
        logger.info(f"Initialized Amadeus fetcher with key: {api_key[:8]}...")
    
    def _get_access_token(self) -> str:
        """Get OAuth access token from Amadeus API."""
        if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.access_token
        
        try:
            url = "https://test.api.amadeus.com/v1/security/oauth2/token"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.api_key,
                'client_secret': '4d7fY8brcLFkHMcG'  # Amadeus client secret
            }
            
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.token_expiry = datetime.now() + timedelta(seconds=token_data['expires_in'] - 60)
            
            logger.info("Successfully obtained Amadeus access token")
            return self.access_token
            
        except Exception as e:
            logger.error(f"Error getting access token: {e}")
            return None
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make authenticated request to Amadeus API."""
        try:
            token = self._get_access_token()
            if not token:
                return {}
            
            url = f"{self.base_url}/{endpoint}"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return {}
    
    def search_flights(self, origin: str, destination: str, 
                      departure_date: str, return_date: Optional[str] = None,
                      adults: int = 1, max_price: Optional[int] = None) -> Dict:
        """Search for flights using Amadeus Flight Offers Search API."""
        try:
            params = {
                'originLocationCode': origin,
                'destinationLocationCode': destination,
                'departureDate': departure_date,
                'adults': adults,
                'currencyCode': 'USD',
                'max': 50  # Maximum results
            }
            
            if return_date:
                params['returnDate'] = return_date
            
            if max_price:
                params['maxPrice'] = max_price
            
            logger.info(f"Searching flights: {origin} to {destination} on {departure_date}")
            return self._make_request('shopping/flight-offers', params)
            
        except Exception as e:
            logger.error(f"Error searching flights: {e}")
            return {}
    
    def get_airport_info(self, keyword: str) -> List[Dict]:
        """Get airport/city information using Amadeus Reference Data API."""
        try:
            params = {
                'keyword': keyword,
                'subType': 'AIRPORT,CITY'
            }
            
            logger.info(f"Searching for airports/cities: {keyword}")
            result = self._make_request('reference-data/locations', params)
            return result.get('data', [])
            
        except Exception as e:
            logger.error(f"Error getting airport info: {e}")
            return []
    
    def get_popular_routes(self) -> List[Dict]:
        """Get popular flight routes for data collection."""
        try:
            # Popular routes to fetch
            popular_routes = [
                {"origin": "JFK", "destination": "LAX", "name": "New York to Los Angeles"},
                {"origin": "JFK", "destination": "CDG", "name": "New York to Paris"},
                {"origin": "JFK", "destination": "LHR", "name": "New York to London"},
                {"origin": "LAX", "destination": "CDG", "name": "Los Angeles to Paris"},
                {"origin": "LAX", "destination": "LHR", "name": "Los Angeles to London"},
                {"origin": "ORD", "destination": "CDG", "name": "Chicago to Paris"},
                {"origin": "ORD", "destination": "LHR", "name": "Chicago to London"},
                {"origin": "SFO", "destination": "CDG", "name": "San Francisco to Paris"},
                {"origin": "SFO", "destination": "LHR", "name": "San Francisco to London"},
                {"origin": "MIA", "destination": "CDG", "name": "Miami to Paris"}
            ]
            
            all_flights = []
            departure_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            
            for route in popular_routes:
                try:
                    logger.info(f"Fetching flights for {route['name']}")
                    
                    flights = self.search_flights(
                        route['origin'], 
                        route['destination'], 
                        departure_date
                    )
                    
                    if flights.get('data'):
                        for flight in flights['data']:
                            flight['route_name'] = route['name']
                            flight['origin'] = route['origin']
                            flight['destination'] = route['destination']
                            all_flights.append(flight)
                    
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    logger.warning(f"Error fetching route {route['name']}: {e}")
                    continue
            
            logger.info(f"Successfully fetched {len(all_flights)} flight offers")
            return all_flights
            
        except Exception as e:
            logger.error(f"Error fetching popular routes: {e}")
            return []
    
    def get_flight_offers_pricing(self, flight_offers: List[Dict]) -> List[Dict]:
        """Get detailed pricing for flight offers."""
        try:
            if not flight_offers:
                return []
            
            url = f"{self.base_url}/shopping/flight-offers/pricing"
            token = self._get_access_token()
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'data': {
                    'type': 'flight-offers-pricing',
                    'flightOffers': flight_offers
                }
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result.get('data', {}).get('flightOffers', [])
            
        except Exception as e:
            logger.error(f"Error getting flight pricing: {e}")
            return flight_offers  # Return original data if pricing fails
    
    def get_airline_info(self, airline_code: str) -> Dict:
        """Get airline information."""
        try:
            params = {
                'airlineCodes': airline_code
            }
            
            result = self._make_request('reference-data/airlines', params)
            airlines = result.get('data', [])
            return airlines[0] if airlines else {}
            
        except Exception as e:
            logger.error(f"Error getting airline info: {e}")
            return {}
    
    def get_airport_autocomplete(self, keyword: str) -> List[Dict]:
        """Get airport autocomplete suggestions."""
        try:
            params = {
                'keyword': keyword,
                'subType': 'AIRPORT,CITY'
            }
            
            result = self._make_request('reference-data/locations', params)
            return result.get('data', [])
            
        except Exception as e:
            logger.error(f"Error getting airport autocomplete: {e}")
            return []

def main():
    """Test the Amadeus API integration."""
    print("🧪 Testing Amadeus API Integration")
    print("=" * 50)
    
    # Initialize fetcher with the provided API key
    fetcher = AmadeusFetcher("8W8ZGIcN61pNWmljxuc350cSGFUGXTCv")
    
    try:
        # Test 1: Airport autocomplete
        print("\n1. Testing airport autocomplete...")
        airports = fetcher.get_airport_autocomplete("New York")
        if airports:
            print(f"✅ Found {len(airports)} airports/cities for 'New York'")
            for airport in airports[:3]:
                print(f"   - {airport.get('name', 'N/A')} ({airport.get('iataCode', 'N/A')})")
        else:
            print("❌ No airports found")
        
        # Test 2: Flight search (limited to avoid rate limits)
        print("\n2. Testing flight search...")
        departure_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        flights = fetcher.search_flights("JFK", "LAX", departure_date, max_price=1000)
        
        if flights.get('data'):
            print(f"✅ Found {len(flights['data'])} flights from JFK to LAX")
            
            # Show sample flight data
            for i, flight in enumerate(flights['data'][:2]):
                print(f"   Flight {i+1}:")
                print(f"     Price: ${flight.get('price', {}).get('total', 'N/A')}")
                print(f"     Stops: {len(flight.get('itineraries', [{}])[0].get('segments', [])) - 1}")
                print(f"     Duration: {flight.get('itineraries', [{}])[0].get('duration', 'N/A')}")
        else:
            print("❌ No flights found")
        
        print("\n🎉 Amadeus API integration test completed!")
        print("\n📝 Note: You'll need to:")
        print("   1. Get your client secret from Amadeus developer portal")
        print("   2. Update the client_secret in the _get_access_token method")
        print("   3. Consider upgrading to production API for more features")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main() 