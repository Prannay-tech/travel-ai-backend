-- AI Travel Advisor Database Schema (Complete)
-- Run this in your Supabase SQL Editor

-- Create Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" SCHEMA extensions;

-- Users Table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Travel Sessions Table
CREATE TABLE IF NOT EXISTS public.travel_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    session_name TEXT,
    destination TEXT,
    start_date DATE,
    end_date DATE,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'archived')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chat Messages Table
CREATE TABLE IF NOT EXISTS public.chat_messages (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id UUID REFERENCES public.travel_sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    message_type TEXT NOT NULL CHECK (message_type IN ('user', 'ai', 'system')),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Travel Preferences Table
CREATE TABLE IF NOT EXISTS public.travel_preferences (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    preferred_destinations JSONB,
    budget_range NUMRANGE,
    travel_style TEXT[],
    accommodation_type TEXT,
    num_travelers INTEGER DEFAULT 1,
    preferred_currency TEXT DEFAULT 'USD',
    flight_class_preference TEXT DEFAULT 'economy' CHECK (flight_class_preference IN ('economy', 'premium_economy', 'business', 'first')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Destinations Table (for storing destination data)
CREATE TABLE IF NOT EXISTS public.destinations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    city TEXT,
    region TEXT,
    destination_type TEXT[],
    description TEXT,
    image_url TEXT,
    coordinates POINT,
    timezone TEXT,
    currency TEXT,
    language TEXT[],
    best_time_to_visit JSONB,
    visa_requirements JSONB,
    safety_info JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Flight Routes Table
CREATE TABLE IF NOT EXISTS public.flight_routes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    origin_airport TEXT NOT NULL,
    destination_airport TEXT NOT NULL,
    origin_city TEXT,
    destination_city TEXT,
    origin_country TEXT,
    destination_country TEXT,
    distance_km INTEGER,
    avg_duration_minutes INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Flight Costs Table
CREATE TABLE IF NOT EXISTS public.flight_costs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    route_id UUID REFERENCES public.flight_routes(id) ON DELETE CASCADE,
    flight_class TEXT NOT NULL CHECK (flight_class IN ('economy', 'premium_economy', 'business', 'first')),
    airline TEXT,
    price DECIMAL(10,2) NOT NULL,
    currency TEXT DEFAULT 'USD',
    departure_date DATE,
    return_date DATE,
    duration_minutes INTEGER,
    stops INTEGER DEFAULT 0,
    source TEXT, -- Which API provided this data
    cached_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Accommodation Types Table
CREATE TABLE IF NOT EXISTS public.accommodation_types (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL CHECK (category IN ('hotel', 'hostel', 'apartment', 'resort', 'camping', 'guesthouse')),
    description TEXT,
    typical_amenities TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Accommodation Costs Table
CREATE TABLE IF NOT EXISTS public.accommodation_costs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    destination_id UUID REFERENCES public.destinations(id) ON DELETE CASCADE,
    accommodation_type_id UUID REFERENCES public.accommodation_types(id) ON DELETE CASCADE,
    property_name TEXT NOT NULL,
    price_per_night DECIMAL(10,2) NOT NULL,
    currency TEXT DEFAULT 'USD',
    rating DECIMAL(3,2),
    amenities TEXT[],
    location_coordinates POINT,
    room_type TEXT,
    max_guests INTEGER,
    source TEXT,
    cached_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Activity Categories Table
CREATE TABLE IF NOT EXISTS public.activity_categories (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    icon TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Activity Costs Table
CREATE TABLE IF NOT EXISTS public.activity_costs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    destination_id UUID REFERENCES public.destinations(id) ON DELETE CASCADE,
    category_id UUID REFERENCES public.activity_categories(id) ON DELETE CASCADE,
    activity_name TEXT NOT NULL,
    price_range JSONB, -- {min, max}
    currency TEXT DEFAULT 'USD',
    duration_hours DECIMAL(4,2),
    description TEXT,
    difficulty_level TEXT CHECK (difficulty_level IN ('easy', 'moderate', 'hard')),
    source TEXT,
    cached_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transportation Options Table
CREATE TABLE IF NOT EXISTS public.transportation_options (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    destination_id UUID REFERENCES public.destinations(id) ON DELETE CASCADE,
    transport_type TEXT NOT NULL CHECK (transport_type IN ('public', 'taxi', 'rental_car', 'bike', 'walking')),
    avg_cost_per_day DECIMAL(10,2),
    currency TEXT DEFAULT 'USD',
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Favorites Table
CREATE TABLE IF NOT EXISTS public.user_favorites (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    destination TEXT,
    notes TEXT,
    rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Travel History Table
CREATE TABLE IF NOT EXISTS public.travel_history (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    destination TEXT NOT NULL,
    trip_start_date DATE,
    trip_end_date DATE,
    total_cost NUMERIC(10,2),
    currency TEXT DEFAULT 'USD',
    rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Recommendations Table
CREATE TABLE IF NOT EXISTS public.ai_recommendations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    destination TEXT NOT NULL,
    recommendation_type TEXT,
    details JSONB,
    confidence_score NUMERIC(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Cost Estimates Table
CREATE TABLE IF NOT EXISTS public.cost_estimates (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    destination TEXT NOT NULL,
    estimated_total_cost NUMERIC(10,2),
    breakdown JSONB,
    currency TEXT DEFAULT 'USD',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- System Logs Table
CREATE TABLE IF NOT EXISTS public.system_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    log_type TEXT NOT NULL,
    log_message TEXT NOT NULL,
    severity TEXT CHECK (severity IN ('info', 'warning', 'error')),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for Performance
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_travel_sessions_user ON public.travel_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session ON public.chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_user ON public.chat_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_travel_preferences_user ON public.travel_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_destinations_name ON public.destinations(name);
CREATE INDEX IF NOT EXISTS idx_destinations_country ON public.destinations(country);
CREATE INDEX IF NOT EXISTS idx_destinations_type ON public.destinations USING gin(destination_type);
CREATE INDEX IF NOT EXISTS idx_flight_routes_route ON public.flight_routes(origin_airport, destination_airport);
CREATE INDEX IF NOT EXISTS idx_flight_costs_route_class ON public.flight_costs(route_id, flight_class);
CREATE INDEX IF NOT EXISTS idx_flight_costs_price ON public.flight_costs(price);
CREATE INDEX IF NOT EXISTS idx_accommodation_costs_destination ON public.accommodation_costs(destination_id);
CREATE INDEX IF NOT EXISTS idx_accommodation_costs_price ON public.accommodation_costs(price_per_night);
CREATE INDEX IF NOT EXISTS idx_activity_costs_destination ON public.activity_costs(destination_id);
CREATE INDEX IF NOT EXISTS idx_user_favorites_user ON public.user_favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_travel_history_user ON public.travel_history(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_user ON public.ai_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_cost_estimates_user ON public.cost_estimates(user_id);
CREATE INDEX IF NOT EXISTS idx_system_logs_user ON public.system_logs(user_id);

-- Row Level Security (RLS) Policies
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.travel_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.travel_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_favorites ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.travel_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.cost_estimates ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.system_logs ENABLE ROW LEVEL SECURITY;

-- Users policies
CREATE POLICY "Users can view and edit their own profile" 
ON public.users FOR ALL 
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);

-- Travel sessions policies
CREATE POLICY "Users can view own sessions" 
ON public.travel_sessions FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own sessions" 
ON public.travel_sessions FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own sessions" 
ON public.travel_sessions FOR UPDATE 
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own sessions" 
ON public.travel_sessions FOR DELETE 
USING (auth.uid() = user_id);

-- Chat messages policies
CREATE POLICY "Users can view own chat messages" 
ON public.chat_messages FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own chat messages" 
ON public.chat_messages FOR INSERT 
WITH CHECK (auth.uid() = user_id);

-- Travel preferences policies
CREATE POLICY "Users can view own preferences" 
ON public.travel_preferences FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own preferences" 
ON public.travel_preferences FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own preferences" 
ON public.travel_preferences FOR UPDATE 
USING (auth.uid() = user_id);

-- User favorites policies
CREATE POLICY "Users can view own favorites" 
ON public.user_favorites FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own favorites" 
ON public.user_favorites FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own favorites" 
ON public.user_favorites FOR UPDATE 
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own favorites" 
ON public.user_favorites FOR DELETE 
USING (auth.uid() = user_id);

-- Travel history policies
CREATE POLICY "Users can view own history" 
ON public.travel_history FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own history" 
ON public.travel_history FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own history" 
ON public.travel_history FOR UPDATE 
USING (auth.uid() = user_id);

-- AI recommendations policies
CREATE POLICY "Users can view own recommendations" 
ON public.ai_recommendations FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own recommendations" 
ON public.ai_recommendations FOR INSERT 
WITH CHECK (auth.uid() = user_id);

-- Cost estimates policies
CREATE POLICY "Users can view own cost estimates" 
ON public.cost_estimates FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own cost estimates" 
ON public.cost_estimates FOR INSERT 
WITH CHECK (auth.uid() = user_id);

-- System logs policies
CREATE POLICY "Users can view own logs" 
ON public.system_logs FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own logs" 
ON public.system_logs FOR INSERT 
WITH CHECK (auth.uid() = user_id);

-- Helper function to create new travel session
CREATE OR REPLACE FUNCTION create_new_travel_session(
    user_uuid UUID,
    session_name TEXT DEFAULT NULL,
    destination TEXT DEFAULT NULL,
    start_date DATE DEFAULT NULL,
    end_date DATE DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    session_uuid UUID;
BEGIN
    -- Close any existing active sessions for this user
    UPDATE public.travel_sessions 
    SET status = 'completed', updated_at = NOW()
    WHERE user_id = user_uuid AND status = 'active';
    
    -- Create new session
    INSERT INTO public.travel_sessions (user_id, session_name, destination, start_date, end_date, status)
    VALUES (user_uuid, session_name, destination, start_date, end_date, 'active')
    RETURNING id INTO session_uuid;
    
    RETURN session_uuid;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Helper function to get current active session
CREATE OR REPLACE FUNCTION get_current_travel_session(user_uuid UUID)
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

-- Function to calculate total trip cost
CREATE OR REPLACE FUNCTION calculate_trip_cost(
    destination_name TEXT,
    start_date DATE,
    end_date DATE,
    num_travelers INTEGER DEFAULT 1,
    flight_class TEXT DEFAULT 'economy',
    accommodation_type TEXT DEFAULT 'hotel'
)
RETURNS JSONB AS $$
DECLARE
    trip_duration INTEGER;
    flight_cost DECIMAL(10,2) := 0;
    accommodation_cost DECIMAL(10,2) := 0;
    activity_cost DECIMAL(10,2) := 0;
    transport_cost DECIMAL(10,2) := 0;
    total_cost DECIMAL(10,2) := 0;
    cost_breakdown JSONB;
BEGIN
    -- Calculate trip duration
    trip_duration := end_date - start_date;
    
    -- Get flight cost (mock calculation - replace with real API calls)
    flight_cost := 500.00 * num_travelers; -- Base cost per person
    
    -- Adjust for flight class
    CASE flight_class
        WHEN 'premium_economy' THEN flight_cost := flight_cost * 1.5;
        WHEN 'business' THEN flight_cost := flight_cost * 3.0;
        WHEN 'first' THEN flight_cost := flight_cost * 5.0;
        ELSE flight_cost := flight_cost * 1.0; -- economy
    END CASE;
    
    -- Get accommodation cost (mock calculation)
    accommodation_cost := 150.00 * trip_duration * num_travelers; -- Base cost per night per person
    
    -- Adjust for accommodation type
    CASE accommodation_type
        WHEN 'hostel' THEN accommodation_cost := accommodation_cost * 0.5;
        WHEN 'apartment' THEN accommodation_cost := accommodation_cost * 0.8;
        WHEN 'resort' THEN accommodation_cost := accommodation_cost * 2.0;
        ELSE accommodation_cost := accommodation_cost * 1.0; -- hotel
    END CASE;
    
    -- Get activity cost (mock calculation)
    activity_cost := 50.00 * trip_duration * num_travelers;
    
    -- Get transport cost (mock calculation)
    transport_cost := 30.00 * trip_duration * num_travelers;
    
    -- Calculate total
    total_cost := flight_cost + accommodation_cost + activity_cost + transport_cost;
    
    -- Build breakdown
    cost_breakdown := jsonb_build_object(
        'flight_cost', flight_cost,
        'accommodation_cost', accommodation_cost,
        'activity_cost', activity_cost,
        'transport_cost', transport_cost,
        'total_cost', total_cost,
        'trip_duration', trip_duration,
        'num_travelers', num_travelers,
        'currency', 'USD'
    );
    
    RETURN cost_breakdown;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Insert sample data
INSERT INTO public.accommodation_types (name, category, description, typical_amenities) VALUES
('Budget Hotel', 'hotel', 'Affordable hotel accommodation', ARRAY['WiFi', 'TV', 'Private Bathroom']),
('Luxury Hotel', 'hotel', 'High-end hotel with premium amenities', ARRAY['WiFi', 'TV', 'Private Bathroom', 'Room Service', 'Spa', 'Pool']),
('Hostel', 'hostel', 'Budget-friendly shared accommodation', ARRAY['WiFi', 'Shared Kitchen', 'Common Area']),
('Apartment', 'apartment', 'Self-contained rental unit', ARRAY['WiFi', 'Kitchen', 'Living Room', 'Private Bathroom']),
('Resort', 'resort', 'All-inclusive resort accommodation', ARRAY['WiFi', 'Pool', 'Spa', 'Restaurant', 'Activities']),
('Camping', 'camping', 'Outdoor camping accommodation', ARRAY['Tent', 'Sleeping Bag', 'Campfire']),
('Guesthouse', 'guesthouse', 'Small family-run accommodation', ARRAY['WiFi', 'Private Bathroom', 'Breakfast'])
ON CONFLICT (name) DO NOTHING;

INSERT INTO public.activity_categories (name, description, icon) VALUES
('Cultural', 'Museums, historical sites, and cultural experiences', '🏛️'),
('Adventure', 'Hiking, climbing, and outdoor activities', '🏔️'),
('Relaxation', 'Spa, beach, and wellness activities', '🏖️'),
('Food & Dining', 'Restaurants, cooking classes, and food tours', '🍽️'),
('Entertainment', 'Shows, nightlife, and entertainment venues', '🎭'),
('Shopping', 'Markets, malls, and shopping districts', '🛍️'),
('Transportation', 'Public transport, tours, and transportation', '🚌')
ON CONFLICT (name) DO NOTHING; 