"""
Vector search functionality using pgvector in Supabase.
"""

import numpy as np
from typing import List, Dict, Any, Optional
import logging
from sentence_transformers import SentenceTransformer
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorSearch:
    def __init__(self, supabase_client, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize vector search with Supabase client and embedding model."""
        self.supabase = supabase_client
        self.model = SentenceTransformer(model_name)
        logger.info(f"Initialized vector search with model: {model_name}")
    
    def create_embeddings_table(self):
        """Create the embeddings table with pgvector extension."""
        sql = """
        -- Enable pgvector extension
        CREATE EXTENSION IF NOT EXISTS vector;
        
        -- Create embeddings table with vector column
        CREATE TABLE IF NOT EXISTS embeddings (
            id SERIAL PRIMARY KEY,
            record_id TEXT NOT NULL,
            record_type TEXT NOT NULL,
            embedding vector(384),  -- Dimension for all-MiniLM-L6-v2
            text_for_embedding TEXT,
            metadata JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Create index for vector similarity search
        CREATE INDEX IF NOT EXISTS embeddings_vector_idx 
        ON embeddings 
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
        
        -- Create index for record lookup
        CREATE INDEX IF NOT EXISTS embeddings_record_idx 
        ON embeddings (record_id, record_type);
        """
        
        try:
            self.supabase.rpc('exec_sql', {'sql': sql}).execute()
            logger.info("Created embeddings table with pgvector support")
        except Exception as e:
            logger.error(f"Error creating embeddings table: {e}")
    
    def insert_embeddings(self, records: List[Dict]) -> bool:
        """Insert embeddings into the database."""
        try:
            for record in records:
                # Generate embedding
                text = record.get('text_for_embedding', '')
                if not text:
                    continue
                
                embedding = self.model.encode([text])[0]
                
                # Prepare data for insertion
                data = {
                    'record_id': record['record_id'],
                    'record_type': record['record_type'],
                    'embedding': embedding.tolist(),
                    'text_for_embedding': text,
                    'metadata': record.get('metadata', {})
                }
                
                # Insert into database
                result = self.supabase.table('embeddings').insert(data).execute()
                
                if not result.data:
                    logger.warning(f"Failed to insert embedding for {record['record_id']}")
            
            logger.info(f"Inserted {len(records)} embeddings")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting embeddings: {e}")
            return False
    
    def search_similar(self, query: str, record_type: str = None, 
                      limit: int = 10, similarity_threshold: float = 0.5) -> List[Dict]:
        """Search for similar records using vector similarity."""
        try:
            # Generate embedding for query
            query_embedding = self.model.encode([query])[0]
            
            # Build SQL query
            sql = """
            SELECT 
                e.record_id,
                e.record_type,
                e.text_for_embedding,
                e.metadata,
                1 - (e.embedding <=> $1) as similarity_score
            FROM embeddings e
            WHERE 1 - (e.embedding <=> $1) > $2
            """
            
            params = [query_embedding.tolist(), similarity_threshold]
            
            if record_type:
                sql += " AND e.record_type = $3"
                params.append(record_type)
            
            sql += """
            ORDER BY e.embedding <=> $1
            LIMIT $4
            """
            params.append(limit)
            
            # Execute query
            result = self.supabase.rpc('exec_sql', {
                'sql': sql,
                'params': params
            }).execute()
            
            if result.data:
                logger.info(f"Found {len(result.data)} similar records")
                return result.data
            else:
                logger.info("No similar records found")
                return []
                
        except Exception as e:
            logger.error(f"Error in vector search: {e}")
            return []
    
    def search_places_by_description(self, description: str, limit: int = 10) -> List[Dict]:
        """Search for places based on description similarity."""
        return self.search_similar(description, 'place', limit)
    
    def search_flights_by_preferences(self, preferences: str, limit: int = 10) -> List[Dict]:
        """Search for flights based on user preferences."""
        return self.search_similar(preferences, 'flight', limit)
    
    def get_recommendations(self, user_preferences: str, 
                          budget: float = None, 
                          duration: int = None) -> Dict:
        """Get personalized recommendations based on user preferences."""
        try:
            # Search for similar places
            similar_places = self.search_places_by_description(user_preferences, limit=5)
            
            # Search for similar flights
            similar_flights = self.search_flights_by_preferences(user_preferences, limit=5)
            
            # Filter by budget if specified
            if budget and similar_flights:
                filtered_flights = []
                for flight in similar_flights:
                    metadata = flight.get('metadata', {})
                    price = metadata.get('min_price', 0)
                    if price <= budget:
                        filtered_flights.append(flight)
                similar_flights = filtered_flights[:3]  # Limit to 3 flights
            
            # Calculate total cost
            total_cost = 0
            if similar_flights:
                total_cost = sum(
                    flight.get('metadata', {}).get('min_price', 0) 
                    for flight in similar_flights
                )
            
            # Generate itinerary suggestions
            suggestions = self._generate_itinerary_suggestions(
                user_preferences, similar_places, duration
            )
            
            return {
                'places': similar_places,
                'flights': similar_flights,
                'total_cost': total_cost,
                'itinerary_suggestions': suggestions
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {'places': [], 'flights': [], 'total_cost': 0, 'itinerary_suggestions': []}
    
    def _generate_itinerary_suggestions(self, preferences: str, 
                                      places: List[Dict], 
                                      duration: int = None) -> List[str]:
        """Generate itinerary suggestions based on places and preferences."""
        suggestions = []
        
        if not places:
            return suggestions
        
        # Extract key themes from preferences
        preferences_lower = preferences.lower()
        
        if 'culture' in preferences_lower or 'museum' in preferences_lower:
            suggestions.append("Visit museums and cultural sites in the morning to avoid crowds")
        
        if 'food' in preferences_lower or 'restaurant' in preferences_lower:
            suggestions.append("Try local cuisine at recommended restaurants")
        
        if 'nature' in preferences_lower or 'outdoor' in preferences_lower:
            suggestions.append("Plan outdoor activities during good weather")
        
        if 'historic' in preferences_lower or 'history' in preferences_lower:
            suggestions.append("Take guided tours to learn about local history")
        
        # Add duration-based suggestions
        if duration:
            if duration <= 3:
                suggestions.append("Focus on must-see attractions for a short trip")
            elif duration <= 7:
                suggestions.append("Mix popular attractions with local experiences")
            else:
                suggestions.append("Take time to explore off-the-beaten-path locations")
        
        # Add general suggestions
        suggestions.extend([
            "Book popular attractions in advance to avoid long queues",
            "Check local events and festivals during your visit",
            "Use public transportation to experience the city like a local"
        ])
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def batch_insert_embeddings(self, records: List[Dict], batch_size: int = 100) -> bool:
        """Insert embeddings in batches for better performance."""
        try:
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                
                # Generate embeddings for batch
                texts = [r.get('text_for_embedding', '') for r in batch]
                texts = [t for t in texts if t]  # Remove empty texts
                
                if not texts:
                    continue
                
                embeddings = self.model.encode(texts)
                
                # Prepare batch data
                batch_data = []
                for j, record in enumerate(batch):
                    if record.get('text_for_embedding'):
                        batch_data.append({
                            'record_id': record['record_id'],
                            'record_type': record['record_type'],
                            'embedding': embeddings[j].tolist(),
                            'text_for_embedding': record['text_for_embedding'],
                            'metadata': record.get('metadata', {})
                        })
                
                # Insert batch
                if batch_data:
                    result = self.supabase.table('embeddings').insert(batch_data).execute()
                    logger.info(f"Inserted batch {i//batch_size + 1}: {len(batch_data)} embeddings")
            
            return True
            
        except Exception as e:
            logger.error(f"Error in batch insert: {e}")
            return False
    
    def update_embeddings(self, record_id: str, record_type: str, 
                         new_text: str, new_metadata: Dict = None) -> bool:
        """Update embeddings for an existing record."""
        try:
            # Generate new embedding
            new_embedding = self.model.encode([new_text])[0]
            
            # Update data
            update_data = {
                'embedding': new_embedding.tolist(),
                'text_for_embedding': new_text
            }
            
            if new_metadata:
                update_data['metadata'] = new_metadata
            
            # Update in database
            result = self.supabase.table('embeddings').update(update_data).eq(
                'record_id', record_id
            ).eq('record_type', record_type).execute()
            
            if result.data:
                logger.info(f"Updated embedding for {record_id}")
                return True
            else:
                logger.warning(f"No embedding found to update for {record_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating embedding: {e}")
            return False
    
    def delete_embeddings(self, record_id: str, record_type: str = None) -> bool:
        """Delete embeddings for a record."""
        try:
            query = self.supabase.table('embeddings').delete().eq('record_id', record_id)
            
            if record_type:
                query = query.eq('record_type', record_type)
            
            result = query.execute()
            
            if result.data:
                logger.info(f"Deleted embeddings for {record_id}")
                return True
            else:
                logger.warning(f"No embeddings found to delete for {record_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting embeddings: {e}")
            return False

def main():
    """Example usage of VectorSearch."""
    # This would require a Supabase client
    # from supabase import create_client
    # supabase = create_client(url, key)
    # vector_search = VectorSearch(supabase)
    
    print("VectorSearch class ready for use with Supabase and pgvector")

if __name__ == "__main__":
    main() 