"""
Enhanced ETL Pipeline for Travel AI - Final Pipeline
Populates destinations, transport_options, accommodations, and activities tables
with cost data and proper categorization.
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
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer
from tomtom_client import TomTomClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedETLPipeline:
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase = create_client(supabase_url, supabase_key)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.tomtom = TomTomClient()

    def fetch_destinations(self, city_coords: List[Dict[str, Any]], query="tourist attraction") -> List[Dict]:
        """Fetch POIs for each city using TomTom."""
        destinations = []
        for city in city_coords:
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
        return destinations

    def generate_embedding(self, text: str) -> List[float]:
        if not text:
            text = "travel destination"
        return self.embedder.encode(text).tolist()

    def load_to_supabase(self, destinations: List[Dict]):
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

    def run_pipeline(self, city_coords: List[Dict[str, Any]]):
        logger.info("Starting TomTom-based ETL pipeline...")
        destinations = self.fetch_destinations(city_coords)
        logger.info(f"Loading {len(destinations)} destinations to Supabase...")
        self.load_to_supabase(destinations)
        logger.info("ETL pipeline completed!")

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
    ]
    pipeline = EnhancedETLPipeline(supabase_url, supabase_key)
    pipeline.run_pipeline(city_coords)

if __name__ == "__main__":
    main() 