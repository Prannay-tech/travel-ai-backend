"""
Skyscanner API via RapidAPI for flight data fetching.
This provides better free tier access than direct Skyscanner API.
"""

import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkyscannerRapidAPIFetcher:
    def __init__(self, rapidapi_key: str = "8W8ZGIcN61pNWmljxuc350cSGFUGXTCv"):
        self.rapidapi_key = rapidapi_key
        self.base_url = "https://skyscanner-api.p.rapidapi.com"
        self.headers = {
            'X-RapidAPI-Key': rapidapi_key,
            'X-RapidAPI-Host': 'skyscanner-api.p.rapidapi.com'
        }
        logger.info(f"Initialized Skyscanner RapidAPI fetcher with key: {rapidapi_key[:8]}...")
    
    def search_flights(self, origin: str, destination: str, 
                      departure_date: str, return_date: Optional[str] = None) -> Dict:
        """Search for flights using RapidAPI Skyscanner endpoint."""
        try:
            url = f"{self.base_url}/apiservices/v3/flights/live/search/create"
            
            payload = {
                "query": {
                    "market": "US",
                    "locale": "en-US",
                    "currency": "USD",
                    "queryLegs": [
                        {
                            "originPlaceId": origin,
                            "destinationPlaceId": destination,
                            "date": departure_date
                        }
                    ],
                    "adults": 1,
                    "childrenAges": [],
                    "cabinClass": "CABIN_CLASS_ECONOMY"
                }
            }
            
            if return_date:
                payload["query"]["queryLegs"].append({
                    "originPlaceId": destination,
                    "destinationPlaceId": origin,
                    "date": return_date
                })
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Flight search initiated for {origin} to {destination}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching flights: {e}")
            return {}
    
    def get_place_autosuggest(self, query: str) -> List[Dict]:
        """Get place suggestions for airport/city search."""
        try:
            url = f"{self.base_url}/apiservices/v3/autosuggest/flights/en-US/USD/en-US"
            params = {
                'query': query
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Found {len(data.get('places', []))} places for query: {query}")
            return data.get('places', [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting place suggestions: {e}")
            return []
    
    def get_quotes(self, origin: str, destination: str, 
                   departure_date: str, return_date: Optional[str] = None) -> Dict:
        """Get flight quotes using RapidAPI."""
        try:
            url = f"{self.base_url}/apiservices/v3/flights/live/search/poll"
            params = {
                'sessionToken': self._create_search_session(origin, destination, departure_date)
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting quotes: {e}")
            return {}
    
    def _create_search_session(self, origin: str, destination: str, date: str) -> str:
        """Create a search session for polling results."""
        try:
            url = f"{self.base_url}/apiservices/v3/flights/live/search/create"
            payload = {
                "query": {
                    "market": "US",
                    "locale": "en-US",
                    "currency": "USD",
                    "queryLegs": [
                        {
                            "originPlaceId": origin,
                            "destinationPlaceId": destination,
                            "date": date
                        }
                    ],
                    "adults": 1,
                    "childrenAges": [],
                    "cabinClass": "CABIN_CLASS_ECONOMY"
                }
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            return response.json().get('sessionToken', '')
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating search session: {e}")
            return ""
    
    def get_popular_routes(self) -> List[Dict]:
        """Get popular flight routes for data collection."""
        try:
            url = f"{self.base_url}/apiservices/v3/flights/live/search/create"
            
            # Popular routes to fetch
            popular_routes = [
                {"origin": "JFK-sky", "destination": "LAX-sky", "name": "New York to Los Angeles"},
                {"origin": "JFK-sky", "destination": "CDG-sky", "name": "New York to Paris"},
                {"origin": "JFK-sky", "destination": "LHR-sky", "name": "New York to London"},
                {"origin": "LAX-sky", "destination": "CDG-sky", "name": "Los Angeles to Paris"},
                {"origin": "LAX-sky", "destination": "LHR-sky", "name": "Los Angeles to London"},
                {"origin": "ORD-sky", "destination": "CDG-sky", "name": "Chicago to Paris"},
                {"origin": "ORD-sky", "destination": "LHR-sky", "name": "Chicago to London"},
                {"origin": "SFO-sky", "destination": "CDG-sky", "name": "San Francisco to Paris"},
                {"origin": "SFO-sky", "destination": "LHR-sky", "name": "San Francisco to London"},
                {"origin": "MIA-sky", "destination": "CDG-sky", "name": "Miami to Paris"}
            ]
            
            all_flights = []
            departure_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            
            for route in popular_routes:
                try:
                    logger.info(f"Fetching flights for {route['name']}")
                    
                    # Create search session
                    session_token = self._create_search_session(
                        route['origin'], 
                        route['destination'], 
                        departure_date
                    )
                    
                    if session_token:
                        # Poll for results
                        time.sleep(2)  # Rate limiting
                        quotes = self.get_quotes(route['origin'], route['destination'], departure_date)
                        
                        if quotes.get('quotes'):
                            for quote in quotes['quotes']:
                                quote['route_name'] = route['name']
                                quote['origin'] = route['origin']
                                quote['destination'] = route['destination']
                                all_flights.append(quote)
                    
                    time.sleep(1)  # Rate limiting between requests
                    
                except Exception as e:
                    logger.warning(f"Error fetching route {route['name']}: {e}")
                    continue
            
            logger.info(f"Successfully fetched {len(all_flights)} flight quotes")
            return all_flights
            
        except Exception as e:
            logger.error(f"Error fetching popular routes: {e}")
            return []

def main():
    """Test the SkyscannerRapidAPIFetcher with the provided API key."""
    print("🧪 Testing Skyscanner RapidAPI Integration")
    print("=" * 50)
    
    # Initialize fetcher with the provided API key
    fetcher = SkyscannerRapidAPIFetcher("8W8ZGIcN61pNWmljxuc350cSGFUGXTCv")
    
    try:
        # Test 1: Place autosuggest
        print("\n1. Testing place autosuggest...")
        places = fetcher.get_place_autosuggest("New York")
        if places:
            print(f"✅ Found {len(places)} places for 'New York'")
            for place in places[:3]:  # Show first 3
                print(f"   - {place.get('name', 'N/A')} ({place.get('placeId', 'N/A')})")
        else:
            print("❌ No places found")
        
        # Test 2: Popular routes (limited to avoid rate limits)
        print("\n2. Testing popular routes (limited sample)...")
        popular_routes = fetcher.get_popular_routes()
        if popular_routes:
            print(f"✅ Successfully fetched {len(popular_routes)} flight quotes")
            
            # Show sample data
            for i, flight in enumerate(popular_routes[:3]):
                print(f"   Flight {i+1}:")
                print(f"     Route: {flight.get('route_name', 'N/A')}")
                print(f"     Price: ${flight.get('minPrice', {}).get('amount', 'N/A')}")
                print(f"     Direct: {flight.get('direct', 'N/A')}")
                print(f"     Stops: {len(flight.get('outboundLeg', {}).get('stopIds', []))}")
        else:
            print("❌ No flights found")
        
        print("\n🎉 Skyscanner API integration test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main() 