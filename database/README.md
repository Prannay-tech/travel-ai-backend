# Database Setup Guide

This guide will help you set up the complete database schema for the AI Travel Advisor project in Supabase.

## Prerequisites

1. **Supabase Account**: You need a Supabase account and project
2. **Environment Variables**: Make sure you have your Supabase credentials in your `.env` file:
   ```
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
   ```

## Option 1: Manual Setup (Recommended)

### Step 1: Access Supabase Dashboard
1. Go to [supabase.com](https://supabase.com) and sign in
2. Select your project
3. Navigate to the **SQL Editor** in the left sidebar

### Step 2: Run the Schema
1. Open the `database/schema.sql` file in your project
2. Copy the entire contents
3. Paste it into the SQL Editor in Supabase
4. Click **Run** to execute the schema

### Step 3: Verify Setup
1. Go to **Table Editor** in the left sidebar
2. You should see all the tables listed:
   - `users`
   - `travel_sessions`
   - `chat_messages`
   - `travel_preferences`
   - `destinations`
   - `points_of_interest`
   - `flight_costs`
   - `accommodation_costs`
   - `activity_costs`
   - `ai_recommendations`
   - `cost_estimates`
   - `user_favorites`
   - `travel_history`
   - `data_sources`
   - `system_logs`

## Option 2: Automated Setup

### Install Dependencies
```bash
pip install supabase python-dotenv
```

### Run the Setup Script
```bash
# Navigate to the database directory
cd database

# Run the setup script
python setup_database.py all
```

The script will:
1. Connect to your Supabase instance
2. Execute the schema SQL
3. Verify the setup
4. Insert sample data

## Database Schema Overview

### Core Tables

#### Users
- Extends Supabase auth.users
- Stores user profile information and preferences

#### Travel Sessions
- Manages user travel planning sessions
- Tracks active/completed/archived sessions

#### Chat Messages
- Stores all chat interactions between users and AI
- Supports user, AI, and system message types

#### Travel Preferences
- Stores user travel preferences collected during chat
- Includes budget, dates, destination type, etc.

### Data Tables

#### Destinations
- Comprehensive destination information
- Includes coordinates, timezone, currency, languages
- Supports multiple destination types

#### Points of Interest
- POIs for each destination
- Includes ratings, price levels, opening hours
- Links to external API data

#### Cost Tables
- `flight_costs`: Flight pricing data
- `accommodation_costs`: Hotel and accommodation pricing
- `activity_costs`: Activity and attraction pricing

### AI & Recommendations

#### AI Recommendations
- Stores AI-generated travel recommendations
- Includes confidence scores and reasoning
- Links to cost estimates

#### Cost Estimates
- Detailed cost breakdowns for recommendations
- Supports multiple cost types (flight, accommodation, etc.)

### User Data

#### User Favorites
- User-saved destinations and POIs
- Supports different favorite types

#### Travel History
- User's past trips and experiences
- Includes ratings, reviews, and photos

### System Tables

#### Data Sources
- Tracks external API integrations
- Includes rate limits and status

#### System Logs
- Application logging and debugging
- Supports different log levels

## Features

### Row Level Security (RLS)
- All user data is protected with RLS policies
- Users can only access their own data
- Secure by default

### Indexes
- Optimized for common queries
- Full-text search on destination names
- Geographic indexes for location-based queries

### Triggers
- Automatic `updated_at` timestamp updates
- Maintains data consistency

### Helper Functions
- `get_current_session()`: Get user's active session
- `create_new_session()`: Create new travel session

## Sample Data

The schema includes sample destinations:
- **Bali**: Beach, cultural, relaxing destination
- **Swiss Alps**: Mountain, adventure destination  
- **Tokyo**: City, cultural destination

## Testing the Setup

### Verify Tables Exist
```sql
-- Check if tables were created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE';
```

### Test RLS Policies
```sql
-- This should only return your own data
SELECT * FROM travel_sessions WHERE user_id = auth.uid();
```

### Test Helper Functions
```sql
-- Create a new session
SELECT create_new_session(auth.uid(), 'Test Session');

-- Get current session
SELECT get_current_session(auth.uid());
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   - Make sure you're using the service role key for admin operations
   - Check that RLS policies are correctly configured

2. **Extensions Not Found**
   - The schema requires `uuid-ossp` and `pg_trgm` extensions
   - These should be available by default in Supabase

3. **Duplicate Key Errors**
   - The schema uses `IF NOT EXISTS` to prevent conflicts
   - If you get duplicate errors, the table already exists

### Reset Database
If you need to start over:
```sql
-- Drop all tables (WARNING: This will delete all data)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
```

Then re-run the schema setup.

## Next Steps

After setting up the database:

1. **Update Backend**: Configure your FastAPI backend to use Supabase
2. **Update Frontend**: Connect your React app to Supabase
3. **Test Integration**: Verify that data flows correctly
4. **Add Real Data**: Populate with real destination data
5. **Monitor**: Use the system_logs table for monitoring

## Support

If you encounter issues:
1. Check the Supabase logs in your dashboard
2. Verify your environment variables
3. Test with the verification script: `python setup_database.py verify`
4. Check the system_logs table for error messages 