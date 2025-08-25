"""
Database setup script for Supabase with user-centric Travel AI schema.
"""

import os
import sys
from supabase.client import create_client, Client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_supabase_database(supabase_url: str, supabase_key: str):
    """Set up the complete database schema with user-centric design."""
    
    try:
        # Initialize Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        logger.info("Connected to Supabase")
        
        # Read the schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute the schema
        logger.info("Executing database schema...")
        result = supabase.rpc('exec_sql', {'sql': schema_sql}).execute()
        logger.info("Schema executed successfully")
        
        # Create additional indexes and functions for the travel data
        additional_sql = """
        -- Enable pgvector extension for embeddings
        CREATE EXTENSION IF NOT EXISTS vector;
        
        -- Create places table for external data
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
            description_processed TEXT,
            travel_tags TEXT,
            sentiment_score DECIMAL(3, 2),
            extracted_locations JSONB,
            extracted_organizations JSONB,
            extracted_dates JSONB,
            extracted_money JSONB,
            extracted_activities JSONB,
            hemisphere TEXT,
            timezone_approx INTEGER,
            continent_approx TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Create flights table for external data
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
            price_category TEXT,
            is_expensive BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Create embeddings table with pgvector
        CREATE TABLE IF NOT EXISTS embeddings (
            id SERIAL PRIMARY KEY,
            record_id TEXT NOT NULL,
            record_type TEXT NOT NULL,
            embedding vector(384),  -- Dimension for all-MiniLM-L6-v2
            text_for_embedding TEXT,
            metadata JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Create indexes for external data
        CREATE INDEX IF NOT EXISTS places_location_idx ON places (latitude, longitude);
        CREATE INDEX IF NOT EXISTS places_rating_idx ON places (rate);
        CREATE INDEX IF NOT EXISTS places_city_idx ON places (city);
        CREATE INDEX IF NOT EXISTS places_country_idx ON places (country);
        CREATE INDEX IF NOT EXISTS places_tags_idx ON places USING GIN (string_to_array(travel_tags, ','));
        
        CREATE INDEX IF NOT EXISTS flights_price_idx ON flights (min_price);
        CREATE INDEX IF NOT EXISTS flights_date_idx ON flights (departure_date);
        CREATE INDEX IF NOT EXISTS flights_route_idx ON flights (origin_id, destination_id);
        
        -- Create vector similarity index
        CREATE INDEX IF NOT EXISTS embeddings_vector_idx 
        ON embeddings 
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
        
        -- Create index for record lookup
        CREATE INDEX IF NOT EXISTS embeddings_record_idx 
        ON embeddings (record_id, record_type);
        
        -- Create full-text search index for places
        CREATE INDEX IF NOT EXISTS places_fts_idx 
        ON places 
        USING GIN (to_tsvector('english', name || ' ' || COALESCE(description, '')));
        
        -- Create functions for similarity search
        CREATE OR REPLACE FUNCTION similarity_search(
            query_embedding vector(384),
            match_threshold float,
            match_count int
        )
        RETURNS TABLE (
            record_id text,
            record_type text,
            similarity_score float
        )
        LANGUAGE plpgsql
        AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                e.record_id,
                e.record_type,
                1 - (e.embedding <=> query_embedding) as similarity_score
            FROM embeddings e
            WHERE 1 - (e.embedding <=> query_embedding) > match_threshold
            ORDER BY e.embedding <=> query_embedding
            LIMIT match_count;
        END;
        $$;
        
        -- Create function for place search with filters
        CREATE OR REPLACE FUNCTION search_places(
            search_query text,
            min_rating float DEFAULT 0,
            max_price float DEFAULT NULL,
            city_filter text DEFAULT NULL,
            country_filter text DEFAULT NULL
        )
        RETURNS TABLE (
            place_id text,
            name text,
            city text,
            country text,
            rate decimal,
            description text,
            similarity_score float
        )
        LANGUAGE plpgsql
        AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                p.place_id,
                p.name,
                p.city,
                p.country,
                p.rate,
                p.description,
                ts_rank(to_tsvector('english', p.name || ' ' || COALESCE(p.description, '')), 
                       plainto_tsquery('english', search_query)) as similarity_score
            FROM places p
            WHERE p.rate >= min_rating
                AND (city_filter IS NULL OR p.city ILIKE '%' || city_filter || '%')
                AND (country_filter IS NULL OR p.country ILIKE '%' || country_filter || '%')
            ORDER BY similarity_score DESC;
        END;
        $$;
        
        -- Create function for flight search
        CREATE OR REPLACE FUNCTION search_flights(
            origin_filter text DEFAULT NULL,
            destination_filter text DEFAULT NULL,
            max_price float DEFAULT NULL,
            direct_only boolean DEFAULT FALSE
        )
        RETURNS TABLE (
            quote_id text,
            origin_id text,
            destination_id text,
            min_price decimal,
            currency text,
            direct boolean,
            stops integer
        )
        LANGUAGE plpgsql
        AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                f.quote_id,
                f.origin_id,
                f.destination_id,
                f.min_price,
                f.currency,
                f.direct,
                f.stops
            FROM flights f
            WHERE (origin_filter IS NULL OR f.origin_id ILIKE '%' || origin_filter || '%')
                AND (destination_filter IS NULL OR f.destination_id ILIKE '%' || destination_filter || '%')
                AND (max_price IS NULL OR f.min_price <= max_price)
                AND (NOT direct_only OR f.direct = TRUE)
            ORDER BY f.min_price ASC;
        END;
        $$;
        
        -- Create function to get user's current session
        CREATE OR REPLACE FUNCTION get_current_session(user_uuid UUID)
        RETURNS UUID AS $$
        DECLARE
            session_uuid UUID;
        BEGIN
            SELECT id INTO session_uuid
            FROM public.travel_sessions
            WHERE user_id = user_uuid AND status = 'active'
            ORDER BY created_at DESC
            LIMIT 1;
            
            RETURN session_uuid;
        END;
        $$ LANGUAGE plpgsql SECURITY DEFINER;
        
        -- Create function to create new session
        CREATE OR REPLACE FUNCTION create_new_session(user_uuid UUID, session_name TEXT DEFAULT NULL)
        RETURNS UUID AS $$
        DECLARE
            session_uuid UUID;
        BEGIN
            -- Close any existing active sessions
            UPDATE public.travel_sessions 
            SET status = 'completed', updated_at = NOW()
            WHERE user_id = user_uuid AND status = 'active';
            
            -- Create new session
            INSERT INTO public.travel_sessions (user_id, session_name, status)
            VALUES (user_uuid, session_name, 'active')
            RETURNING id INTO session_uuid;
            
            RETURN session_uuid;
        END;
        $$ LANGUAGE plpgsql SECURITY DEFINER;
        
        -- Create updated_at trigger function
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        
        -- Apply updated_at triggers to user tables
        CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        CREATE TRIGGER update_travel_sessions_updated_at BEFORE UPDATE ON public.travel_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        CREATE TRIGGER update_travel_preferences_updated_at BEFORE UPDATE ON public.travel_preferences FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """
        
        # Execute additional SQL
        logger.info("Executing additional database setup...")
        result = supabase.rpc('exec_sql', {'sql': additional_sql}).execute()
        logger.info("Additional setup completed successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Error setting up database: {str(e)}")
        return False

def create_sample_data(supabase: Client):
    """Create sample data for testing."""
    
    try:
        # Sample data SQL
        sample_data_sql = """
        -- Insert sample places (if places table exists and is empty)
        INSERT INTO places (place_id, name, type, city, country, latitude, longitude, rate, description, travel_tags)
        VALUES 
        ('paris_france', 'Paris', 'city', 'Paris', 'France', 48.8566, 2.3522, 4.5, 'The City of Light offers iconic landmarks, world-class museums, and exquisite cuisine.', 'romantic,cultural,historic,food'),
        ('tokyo_japan', 'Tokyo', 'city', 'Tokyo', 'Japan', 35.6762, 139.6503, 4.7, 'A fascinating blend of ultramodern and traditional, offering endless discoveries.', 'modern,cultural,technology,food'),
        ('bali_indonesia', 'Bali', 'island', 'Denpasar', 'Indonesia', -8.3405, 115.0920, 4.6, 'Tropical paradise with beautiful beaches, temples, and vibrant culture.', 'beach,relaxing,cultural,spiritual'),
        ('newyork_usa', 'New York City', 'city', 'New York', 'USA', 40.7128, -74.0060, 4.4, 'The Big Apple offers world-class entertainment, dining, and iconic landmarks.', 'urban,cultural,entertainment,shopping'),
        ('santorini_greece', 'Santorini', 'island', 'Fira', 'Greece', 36.3932, 25.4615, 4.8, 'Stunning volcanic island with breathtaking sunsets and white-washed buildings.', 'romantic,beach,scenic,historic')
        ON CONFLICT (place_id) DO NOTHING;
        
        -- Insert sample flights (if flights table exists and is empty)
        INSERT INTO flights (quote_id, min_price, currency, direct, origin_id, destination_id, departure_date, stops)
        VALUES 
        ('flight_001', 450.00, 'USD', true, 'JFK', 'CDG', '2024-08-15', 0),
        ('flight_002', 380.00, 'USD', false, 'LAX', 'NRT', '2024-08-20', 1),
        ('flight_003', 650.00, 'USD', true, 'SFO', 'DPS', '2024-08-25', 0),
        ('flight_004', 280.00, 'USD', true, 'JFK', 'LAX', '2024-08-30', 0),
        ('flight_005', 520.00, 'USD', false, 'LHR', 'JTR', '2024-09-05', 1)
        ON CONFLICT (quote_id) DO NOTHING;
        """
        
        logger.info("Creating sample data...")
        result = supabase.rpc('exec_sql', {'sql': sample_data_sql}).execute()
        logger.info("Sample data created successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Error creating sample data: {str(e)}")
        return False

def main():
    """Main function to set up the database."""
    
    # Get environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        logger.error("Please set SUPABASE_URL and SUPABASE_KEY environment variables")
        sys.exit(1)
    
    # Set up database
    if setup_supabase_database(supabase_url, supabase_key):
        logger.info("Database setup completed successfully!")
        
        # Create sample data
        supabase: Client = create_client(supabase_url, supabase_key)
        create_sample_data(supabase)
        
    else:
        logger.error("Database setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 