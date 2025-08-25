"""
Main ETL pipeline runner for Travel AI.
Coordinates data fetching, cleaning, embedding generation, and loading.
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
import json

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.fetch_opentripmap import OpenTripMapFetcher
from etl.fetch_amadeus import AmadeusFetcher
from etl.enhanced_clean import EnhancedTravelDataCleaner
from etl.embed_hf import HuggingFaceEmbedder
from etl.load_supabase import SupabaseLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TravelAIETLPipeline:
    def __init__(self):
        """Initialize the ETL pipeline with all components."""
        self.start_time = datetime.now()
        
        # API Keys - using the provided Amadeus key
        self.opentripmap_key = os.getenv("OPENTRIPMAP_API_KEY", "your_opentripmap_key")
        self.amadeus_key = os.getenv("AMADEUS_API_KEY", "8W8ZGIcN61pNWmljxuc350cSGFUGXTCv")
        
        # Supabase configuration
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        
        # Initialize components
        self.opentripmap_fetcher = OpenTripMapFetcher(self.opentripmap_key)
        self.amadeus_fetcher = AmadeusFetcher(self.amadeus_key)
        self.cleaner = EnhancedTravelDataCleaner()
        self.embedding_generator = HuggingFaceEmbedder()
        self.supabase_loader = SupabaseLoader(self.supabase_url, self.supabase_key)
        
        logger.info("ETL Pipeline initialized successfully")
    
    def fetch_places_data(self, cities: List[str] = None) -> List[Dict]:
        """Fetch places data from OpenTripMap."""
        if cities is None:
            cities = [
                "Paris", "London", "New York", "Tokyo", "Rome", 
                "Barcelona", "Amsterdam", "Berlin", "Prague", "Vienna",
                "Budapest", "Florence", "Venice", "Madrid", "Lisbon"
            ]
        
        all_places = []
        
        for city in cities:
            try:
                logger.info(f"Fetching places for {city}")
                places = self.opentripmap_fetcher.search_places(city, limit=50)
                all_places.extend(places)
                logger.info(f"Fetched {len(places)} places for {city}")
                
                # Rate limiting
                import time
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error fetching places for {city}: {e}")
                continue
        
        logger.info(f"Total places fetched: {len(all_places)}")
        return all_places
    
    def fetch_flights_data(self) -> List[Dict]:
        """Fetch flights data from Amadeus API."""
        try:
            logger.info("Fetching popular flight routes")
            flights = self.amadeus_fetcher.get_popular_routes()
            logger.info(f"Fetched {len(flights)} flight offers")
            return flights
            
        except Exception as e:
            logger.error(f"Error fetching flights data: {e}")
            return []
    
    def clean_places_data(self, raw_places: List[Dict]) -> List[Dict]:
        """Clean and process places data."""
        try:
            logger.info("Cleaning places data")
            cleaned_places = self.cleaner.clean_opentripmap_data(raw_places)
            
            # Remove duplicates
            cleaned_places = self.cleaner.remove_duplicates(cleaned_places)
            
            # Filter by quality
            cleaned_places = self.cleaner.filter_by_quality(cleaned_places, min_rate=6.0)
            
            # Add geographic features
            cleaned_places = self.cleaner.add_geographic_features(cleaned_places)
            
            logger.info(f"Cleaned {len(cleaned_places)} places")
            return cleaned_places.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error cleaning places data: {e}")
            return []
    
    def clean_flights_data(self, raw_flights: List[Dict]) -> List[Dict]:
        """Clean and process flights data."""
        try:
            logger.info("Cleaning flights data")
            cleaned_flights = self.cleaner.clean_amadeus_data(raw_flights)
            logger.info(f"Cleaned {len(cleaned_flights)} flights")
            return cleaned_flights.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error cleaning flights data: {e}")
            return []
    
    def generate_embeddings(self, places: List[Dict], flights: List[Dict]) -> List[Dict]:
        """Generate embeddings for places and flights using Hugging Face."""
        try:
            logger.info("Generating embeddings")
            # Prepare data for embedding generation
            all_records = []
            texts = []
            for place in places:
                text = f"{place.get('name', '')} {place.get('description', '')} {place.get('travel_tags', '')}"
                all_records.append({
                    'record_id': place.get('place_id', ''),
                    'record_type': 'place',
                    'text_for_embedding': text,
                    'metadata': place
                })
                texts.append(text)
            for flight in flights:
                text = f"{flight.get('route_name', '')} {flight.get('price_category', '')} {'direct' if flight.get('direct') else 'connecting'}"
                all_records.append({
                    'record_id': flight.get('quote_id', ''),
                    'record_type': 'flight',
                    'text_for_embedding': text,
                    'metadata': flight
                })
                texts.append(text)
            # Generate embeddings
            embeddings_np = self.embedding_generator.embed(texts)
            for i, record in enumerate(all_records):
                record['embedding'] = embeddings_np[i].tolist()
            logger.info(f"Generated {len(all_records)} embeddings")
            return all_records
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []
    
    def load_to_supabase(self, places: List[Dict], flights: List[Dict], embeddings: List[Dict]):
        """Load all data to Supabase."""
        try:
            logger.info("Loading data to Supabase")
            
            # Load places
            if places:
                self.supabase_loader.load_places(places)
                logger.info(f"Loaded {len(places)} places")
            
            # Load flights
            if flights:
                self.supabase_loader.load_flights(flights)
                logger.info(f"Loaded {len(flights)} flights")
            
            # Load embeddings
            if embeddings:
                self.supabase_loader.load_embeddings(embeddings)
                logger.info(f"Loaded {len(embeddings)} embeddings")
            
            logger.info("Data loading completed")
            
        except Exception as e:
            logger.error(f"Error loading data to Supabase: {e}")
    
    def run_full_pipeline(self):
        """Run the complete ETL pipeline."""
        logger.info("Starting full ETL pipeline")
        
        try:
            # Step 1: Fetch data
            logger.info("Step 1: Fetching data")
            places_data = self.fetch_places_data()
            flights_data = self.fetch_flights_data()
            
            # Step 2: Clean data
            logger.info("Step 2: Cleaning data")
            cleaned_places = self.clean_places_data(places_data)
            cleaned_flights = self.clean_flights_data(flights_data)
            
            # Step 3: Generate embeddings
            logger.info("Step 3: Generating embeddings")
            embeddings = self.generate_embeddings(cleaned_places, cleaned_flights)
            
            # Step 4: Load to database
            logger.info("Step 4: Loading to database")
            self.load_to_supabase(cleaned_places, cleaned_flights, embeddings)
            
            # Calculate execution time
            execution_time = datetime.now() - self.start_time
            logger.info(f"ETL pipeline completed successfully in {execution_time}")
            
            # Save summary
            self.save_pipeline_summary(cleaned_places, cleaned_flights, embeddings, execution_time)
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {e}")
            raise
    
    def run_places_only(self):
        """Run pipeline for places data only."""
        logger.info("Starting places-only ETL pipeline")
        
        try:
            places_data = self.fetch_places_data()
            cleaned_places = self.clean_places_data(places_data)
            embeddings = self.generate_embeddings(cleaned_places, [])
            self.load_to_supabase(cleaned_places, [], embeddings)
            
            execution_time = datetime.now() - self.start_time
            logger.info(f"Places pipeline completed in {execution_time}")
            
        except Exception as e:
            logger.error(f"Places pipeline failed: {e}")
            raise
    
    def run_flights_only(self):
        """Run pipeline for flights data only."""
        logger.info("Starting flights-only ETL pipeline")
        
        try:
            flights_data = self.fetch_flights_data()
            cleaned_flights = self.clean_flights_data(flights_data)
            embeddings = self.generate_embeddings([], cleaned_flights)
            self.load_to_supabase([], cleaned_flights, embeddings)
            
            execution_time = datetime.now() - self.start_time
            logger.info(f"Flights pipeline completed in {execution_time}")
            
        except Exception as e:
            logger.error(f"Flights pipeline failed: {e}")
            raise
    
    def save_pipeline_summary(self, places: List[Dict], flights: List[Dict], 
                            embeddings: List[Dict], execution_time):
        """Save pipeline execution summary."""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'execution_time_seconds': execution_time.total_seconds(),
            'places_processed': len(places),
            'flights_processed': len(flights),
            'embeddings_generated': len(embeddings),
            'status': 'success'
        }
        
        # Save to file
        with open('pipeline_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Pipeline summary saved: {summary}")

def main():
    """Main entry point for the ETL pipeline."""
    parser = argparse.ArgumentParser(description='Travel AI ETL Pipeline')
    parser.add_argument('--mode', choices=['full', 'places', 'flights'], 
                       default='full', help='Pipeline mode to run')
    parser.add_argument('--test', action='store_true', 
                       help='Run in test mode with limited data')
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = TravelAIETLPipeline()
    
    try:
        if args.mode == 'full':
            pipeline.run_full_pipeline()
        elif args.mode == 'places':
            pipeline.run_places_only()
        elif args.mode == 'flights':
            pipeline.run_flights_only()
        
        logger.info("ETL pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 