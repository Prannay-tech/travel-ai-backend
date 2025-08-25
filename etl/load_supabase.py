"""
Load travel data into Supabase database.
"""

import pandas as pd
import numpy as np
from supabase import create_client, Client
from typing import Dict, List, Any, Optional
import logging
import json
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseLoader:
    def __init__(self, supabase_url: str, supabase_key: str):
        """Initialize Supabase client."""
        self.supabase: Client = create_client(supabase_url, supabase_key)
        logger.info("Initialized Supabase client")
    
    def load_places(self, df: pd.DataFrame, table_name: str = "places") -> bool:
        """Load places data into Supabase."""
        if df.empty:
            logger.warning("Empty dataframe provided for loading")
            return False
        
        try:
            # Prepare data for insertion
            records = self._prepare_places_data(df)
            
            # Insert data in batches
            batch_size = 100
            success_count = 0
            
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                
                result = self.supabase.table(table_name).insert(batch).execute()
                
                if result.data:
                    success_count += len(result.data)
                    logger.info(f"Inserted batch {i//batch_size + 1}: {len(result.data)} records")
                else:
                    logger.error(f"Failed to insert batch {i//batch_size + 1}")
            
            logger.info(f"Successfully loaded {success_count} places into {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading places: {e}")
            return False
    
    def load_flights(self, df: pd.DataFrame, table_name: str = "flights") -> bool:
        """Load flights data into Supabase."""
        if df.empty:
            logger.warning("Empty dataframe provided for loading")
            return False
        
        try:
            # Prepare data for insertion
            records = self._prepare_flights_data(df)
            
            # Insert data in batches
            batch_size = 100
            success_count = 0
            
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                
                result = self.supabase.table(table_name).insert(batch).execute()
                
                if result.data:
                    success_count += len(result.data)
                    logger.info(f"Inserted batch {i//batch_size + 1}: {len(result.data)} records")
                else:
                    logger.error(f"Failed to insert batch {i//batch_size + 1}")
            
            logger.info(f"Successfully loaded {success_count} flights into {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading flights: {e}")
            return False
    
    def load_embeddings(self, df: pd.DataFrame, table_name: str = "embeddings") -> bool:
        """Load embeddings data into Supabase."""
        if df.empty or 'embedding' not in df.columns:
            logger.warning("No embeddings data provided for loading")
            return False
        
        try:
            # Prepare data for insertion
            records = self._prepare_embeddings_data(df)
            
            # Insert data in batches
            batch_size = 50  # Smaller batch size for embeddings
            success_count = 0
            
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                
                result = self.supabase.table(table_name).insert(batch).execute()
                
                if result.data:
                    success_count += len(result.data)
                    logger.info(f"Inserted batch {i//batch_size + 1}: {len(result.data)} records")
                else:
                    logger.error(f"Failed to insert batch {i//batch_size + 1}")
            
            logger.info(f"Successfully loaded {success_count} embeddings into {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading embeddings: {e}")
            return False
    
    def _prepare_places_data(self, df: pd.DataFrame) -> List[Dict]:
        """Prepare places data for Supabase insertion."""
        records = []
        
        for _, row in df.iterrows():
            record = {
                'place_id': row.get('place_id', ''),
                'name': row.get('name', ''),
                'type': row.get('type', ''),
                'categories': row.get('categories', ''),
                'latitude': float(row.get('latitude', 0)) if pd.notna(row.get('latitude')) else None,
                'longitude': float(row.get('longitude', 0)) if pd.notna(row.get('longitude')) else None,
                'country': row.get('country', ''),
                'city': row.get('city', ''),
                'state': row.get('state', ''),
                'postcode': row.get('postcode', ''),
                'street': row.get('street', ''),
                'house_number': row.get('house_number', ''),
                'osm': row.get('osm', ''),
                'wikidata': row.get('wikidata', ''),
                'wikipedia': row.get('wikipedia', ''),
                'rate': float(row.get('rate', 0)) if pd.notna(row.get('rate')) else 0,
                'otm': row.get('otm', ''),
                'sources': row.get('sources', '{}'),
                'extent': row.get('extent', '{}'),
                'url': row.get('url', ''),
                'image': row.get('image', ''),
                'description': row.get('description', ''),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Remove None values
            record = {k: v for k, v in record.items() if v is not None}
            records.append(record)
        
        return records
    
    def _prepare_flights_data(self, df: pd.DataFrame) -> List[Dict]:
        """Prepare flights data for Supabase insertion."""
        records = []
        
        for _, row in df.iterrows():
            record = {
                'quote_id': row.get('quote_id', ''),
                'min_price': float(row.get('min_price', 0)) if pd.notna(row.get('min_price')) else 0,
                'currency': row.get('currency', 'USD'),
                'direct': bool(row.get('direct', False)),
                'outbound_leg': row.get('outbound_leg', '{}'),
                'inbound_leg': row.get('inbound_leg', '{}'),
                'origin_id': row.get('origin_id', ''),
                'destination_id': row.get('destination_id', ''),
                'departure_date': row.get('departure_date', ''),
                'carrier_ids': row.get('carrier_ids', ''),
                'stops': int(row.get('stops', 0)) if pd.notna(row.get('stops')) else 0,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Remove None values
            record = {k: v for k, v in record.items() if v is not None}
            records.append(record)
        
        return records
    
    def _prepare_embeddings_data(self, df: pd.DataFrame) -> List[Dict]:
        """Prepare embeddings data for Supabase insertion."""
        records = []
        
        for _, row in df.iterrows():
            # Convert embedding to list for JSON storage
            embedding = row.get('embedding', [])
            if isinstance(embedding, np.ndarray):
                embedding = embedding.tolist()
            
            record = {
                'record_id': row.get('place_id') or row.get('quote_id', ''),
                'record_type': 'place' if 'place_id' in row else 'flight',
                'embedding': json.dumps(embedding),
                'text_for_embedding': row.get('text_for_embedding', ''),
                'created_at': datetime.now().isoformat()
            }
            
            records.append(record)
        
        return records
    
    def create_tables(self):
        """Create necessary tables in Supabase (SQL to be run manually)."""
        sql_statements = {
            'places': """
                CREATE TABLE IF NOT EXISTS places (
                    id SERIAL PRIMARY KEY,
                    place_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    type TEXT,
                    categories TEXT,
                    latitude DECIMAL(10, 8),
                    longitude DECIMAL(11, 8),
                    country TEXT,
                    city TEXT,
                    state TEXT,
                    postcode TEXT,
                    street TEXT,
                    house_number TEXT,
                    osm TEXT,
                    wikidata TEXT,
                    wikipedia TEXT,
                    rate DECIMAL(3, 2),
                    otm TEXT,
                    sources JSONB,
                    extent JSONB,
                    url TEXT,
                    image TEXT,
                    description TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """,
            'flights': """
                CREATE TABLE IF NOT EXISTS flights (
                    id SERIAL PRIMARY KEY,
                    quote_id TEXT UNIQUE NOT NULL,
                    min_price DECIMAL(10, 2),
                    currency TEXT DEFAULT 'USD',
                    direct BOOLEAN DEFAULT FALSE,
                    outbound_leg JSONB,
                    inbound_leg JSONB,
                    origin_id TEXT,
                    destination_id TEXT,
                    departure_date DATE,
                    carrier_ids TEXT,
                    stops INTEGER DEFAULT 0,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """,
            'embeddings': """
                CREATE TABLE IF NOT EXISTS embeddings (
                    id SERIAL PRIMARY KEY,
                    record_id TEXT NOT NULL,
                    record_type TEXT NOT NULL,
                    embedding JSONB NOT NULL,
                    text_for_embedding TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """
        }
        
        for table_name, sql in sql_statements.items():
            logger.info(f"SQL for creating {table_name} table:")
            print(sql)
            print("\n" + "="*50 + "\n")
    
    def query_similar_places(self, query_embedding: List[float], 
                           limit: int = 5) -> List[Dict]:
        """Query similar places using vector similarity."""
        try:
            # This would require pgvector extension in Supabase
            # For now, we'll return a placeholder
            logger.info("Vector similarity search requires pgvector extension")
            return []
            
        except Exception as e:
            logger.error(f"Error querying similar places: {e}")
            return []

def main():
    """Example usage of SupabaseLoader."""
    # You'll need to set your Supabase credentials
    supabase_url = "YOUR_SUPABASE_URL"
    supabase_key = "YOUR_SUPABASE_KEY"
    
    loader = SupabaseLoader(supabase_url, supabase_key)
    
    # Show table creation SQL
    loader.create_tables()
    
    # Example: Load sample data
    sample_places = pd.DataFrame([
        {
            'place_id': 'test123',
            'name': 'Eiffel Tower',
            'type': 'cultural',
            'categories': 'cultural,historic,architecture',
            'latitude': 48.8584,
            'longitude': 2.2945,
            'country': 'France',
            'city': 'Paris',
            'rate': 7.5,
            'description': 'Iconic iron lattice tower'
        }
    ])
    
    # success = loader.load_places(sample_places)
    # print(f"Load successful: {success}")

if __name__ == "__main__":
    main() 