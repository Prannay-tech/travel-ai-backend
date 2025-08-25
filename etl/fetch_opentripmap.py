"""
OpenTripMap API data fetcher for travel destinations and attractions.
"""

import requests
import json
import time
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenTripMapFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.opentripmap.com/0.1/en/places"
    
    def search_places(self, query: str, limit: int = 50) -> List[Dict]:
        """Search for places using OpenTripMap API."""
        try:
            url = f"{self.base_url}/autosuggest"
            params = {
                'name': query,
                'limit': limit,
                'apikey': self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Found {len(data)} places for query: {query}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for {query}: {e}")
            return []
    
    def get_place_details(self, xid: str) -> Optional[Dict]:
        """Get detailed information about a specific place."""
        try:
            url = f"{self.base_url}/xid/{xid}"
            params = {'apikey': self.api_key}
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching details for xid {xid}: {e}")
            return None
    
    def search_by_coordinates(self, lat: float, lon: float, radius: int = 5000) -> List[Dict]:
        """Search for places around specific coordinates."""
        try:
            url = f"{self.base_url}/radius"
            params = {
                'radius': radius,
                'lon': lon,
                'lat': lat,
                'apikey': self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Found {len(data.get('features', []))} places around coordinates")
            return data.get('features', [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for coordinates {lat}, {lon}: {e}")
            return []

def main():
    """Example usage of OpenTripMapFetcher."""
    # You'll need to set your API key
    api_key = "YOUR_OPENTRIPMAP_API_KEY"
    
    fetcher = OpenTripMapFetcher(api_key)
    
    # Example searches
    places = fetcher.search_places("Paris")
    print(f"Found {len(places)} places in Paris")
    
    # Get details for first place
    if places:
        details = fetcher.get_place_details(places[0]['xid'])
        print(f"Details for {places[0]['name']}: {details}")

if __name__ == "__main__":
    main() 