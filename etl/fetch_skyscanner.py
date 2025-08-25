"""
Skyscanner API data fetcher for flight information.
"""

import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkyscannerFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://partners.api.skyscanner.net/apiservices/v3"
        self.headers = {
            'x-api-key': api_key,
            'Accept': 'application/json'
        }
    
    def search_flights(self, origin: str, destination: str, 
                      outbound_date: str, inbound_date: Optional[str] = None) -> Dict:
        """Search for flights between two locations."""
        try:
            url = f"{self.base_url}/flights/live/search/create"
            
            payload = {
                "query": {
                    "market": "US",
                    "locale": "en-US",
                    "currency": "USD",
                    "queryLegs": [
                        {
                            "originPlaceId": origin,
                            "destinationPlaceId": destination,
                            "date": outbound_date
                        }
                    ],
                    "adults": 1,
                    "childrenAges": [],
                    "cabinClass": "CABIN_CLASS_ECONOMY"
                }
            }
            
            if inbound_date:
                payload["query"]["queryLegs"].append({
                    "originPlaceId": destination,
                    "destinationPlaceId": origin,
                    "date": inbound_date
                })
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Flight search initiated for {origin} to {destination}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching flights: {e}")
            return {}
    
    def get_search_results(self, session_token: str) -> Dict:
        """Get results for a flight search session."""
        try:
            url = f"{self.base_url}/flights/live/search/poll/{session_token}"
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting search results: {e}")
            return {}
    
    def get_place_autosuggest(self, query: str) -> List[Dict]:
        """Get place suggestions for airport/city search."""
        try:
            url = f"{self.base_url}/autosuggest/flights"
            params = {
                'query': query,
                'market': 'US',
                'locale': 'en-US'
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
                   outbound_date: str, inbound_date: Optional[str] = None) -> Dict:
        """Get flight quotes (simplified API)."""
        try:
            url = f"{self.base_url}/flights/indicative/search"
            params = {
                'originSkyId': origin,
                'destinationSkyId': destination,
                'date': outbound_date,
                'returnDate': inbound_date,
                'market': 'US',
                'locale': 'en-US',
                'currency': 'USD'
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting quotes: {e}")
            return {}

def main():
    """Example usage of SkyscannerFetcher."""
    # You'll need to set your API key
    api_key = "YOUR_SKYSCANNER_API_KEY"
    
    fetcher = SkyscannerFetcher(api_key)
    
    # Example: Search for places
    places = fetcher.get_place_autosuggest("New York")
    print(f"Found {len(places)} places for New York")
    
    # Example: Get flight quotes
    outbound_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    quotes = fetcher.get_quotes("JFK-sky", "LAX-sky", outbound_date)
    print(f"Flight quotes: {quotes}")

if __name__ == "__main__":
    main() 