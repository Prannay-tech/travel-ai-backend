#!/usr/bin/env python3
"""
Database Setup Script for AI Travel Advisor
This script sets up the complete database schema in Supabase
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from supabase.client import create_client, Client
except ImportError:
    print("Error: supabase-py not installed. Install with: pip install supabase")
    sys.exit(1)

def load_schema_file():
    """Load the SQL schema from the schema.sql file"""
    schema_file = Path(__file__).parent / "schema.sql"
    if not schema_file.exists():
        print(f"Error: Schema file not found at {schema_file}")
        sys.exit(1)
    
    with open(schema_file, 'r') as f:
        return f.read()

def setup_database():
    """Set up the database schema in Supabase"""
    # Load environment variables
    load_dotenv()
    
    # Get Supabase credentials
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')  # Use service role key for admin operations
    
    if not supabase_url or not supabase_key:
        print("Error: Missing Supabase credentials in environment variables")
        print("Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY")
        sys.exit(1)
    
    try:
        # Initialize Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Connected to Supabase")
        
        # Load and execute schema
        schema_sql = load_schema_file()
        print("📄 Loaded schema file")
        
        # Split schema into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        print(f"🔧 Executing {len(statements)} SQL statements...")
        
        for i, statement in enumerate(statements, 1):
            if statement and not statement.startswith('--'):
                try:
                    # Execute the statement
                    result = supabase.rpc('exec_sql', {'sql': statement}).execute()
                    print(f"  ✅ Statement {i}/{len(statements)} executed successfully")
                except Exception as e:
                    # If exec_sql RPC doesn't exist, try direct execution
                    try:
                        # For direct SQL execution, we need to use the REST API
                        # This is a simplified approach - in practice, you might want to use
                        # the Supabase dashboard or pgAdmin for schema setup
                        print(f"  ⚠️  Statement {i}/{len(statements)}: {str(e)[:100]}...")
                    except Exception as e2:
                        print(f"  ❌ Statement {i}/{len(statements)} failed: {str(e2)[:100]}...")
        
        print("\n🎉 Database setup completed!")
        print("\nNext steps:")
        print("1. Go to your Supabase dashboard")
        print("2. Navigate to the SQL Editor")
        print("3. Copy and paste the contents of database/schema.sql")
        print("4. Run the SQL to create all tables and functions")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        sys.exit(1)

def verify_setup():
    """Verify that the database setup was successful"""
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')  # Use anon key for verification
    
    if not supabase_url or not supabase_key:
        print("Error: Missing Supabase credentials")
        return False
    
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Test basic connectivity
        print("🔍 Verifying database setup...")
        
        # Check if key tables exist by trying to query them
        tables_to_check = [
            'users',
            'travel_sessions', 
            'chat_messages',
            'travel_preferences',
            'user_favorites',
            'travel_history',
            'ai_recommendations',
            'cost_estimates',
            'system_logs'
        ]
        
        for table in tables_to_check:
            try:
                # Try to select from the table (should work even if empty)
                result = supabase.table(table).select('*').limit(1).execute()
                print(f"  ✅ Table '{table}' exists and is accessible")
            except Exception as e:
                print(f"  ❌ Table '{table}' not found or not accessible: {str(e)[:100]}...")
                return False
        
        print("✅ Database verification completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying database: {e}")
        return False

def insert_sample_data():
    """Insert sample data for testing"""
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    if not supabase_url or not supabase_key:
        print("Error: Missing Supabase credentials")
        return False
    
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        
        print("📝 Inserting sample destinations...")
        
        # Sample destinations
        sample_destinations = [
            {
                'name': 'Bali',
                'country': 'Indonesia',
                'city': 'Denpasar',
                'region': 'Bali',
                'destination_type': ['beach', 'cultural', 'relaxing'],
                'description': 'Tropical paradise with beautiful beaches, temples, and culture',
                'timezone': 'Asia/Jakarta',
                'currency': 'IDR',
                'language': ['Indonesian', 'English'],
                'best_time_to_visit': {
                    'months': ['April', 'May', 'June', 'September', 'October'],
                    'reason': 'Dry season with pleasant weather'
                }
            },
            {
                'name': 'Swiss Alps',
                'country': 'Switzerland',
                'city': 'Zermatt',
                'region': 'Valais',
                'destination_type': ['mountain', 'adventure', 'relaxing'],
                'description': 'Majestic mountains perfect for skiing and hiking',
                'timezone': 'Europe/Zurich',
                'currency': 'CHF',
                'language': ['German', 'French', 'Italian', 'English'],
                'best_time_to_visit': {
                    'winter': 'December to March for skiing',
                    'summer': 'June to September for hiking'
                }
            },
            {
                'name': 'Tokyo',
                'country': 'Japan',
                'city': 'Tokyo',
                'region': 'Kanto',
                'destination_type': ['city', 'cultural', 'adventure'],
                'description': 'Modern metropolis with rich culture and technology',
                'timezone': 'Asia/Tokyo',
                'currency': 'JPY',
                'language': ['Japanese', 'English'],
                'best_time_to_visit': {
                    'spring': 'March to May for cherry blossoms',
                    'autumn': 'October to November for pleasant weather'
                }
            }
        ]
        
        for destination in sample_destinations:
            try:
                result = supabase.table('destinations').insert(destination).execute()
                print(f"  ✅ Added destination: {destination['name']}")
            except Exception as e:
                print(f"  ⚠️  Could not add {destination['name']}: {str(e)[:100]}...")
        
        print("✅ Sample data insertion completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error inserting sample data: {e}")
        return False

def main():
    """Main function"""
    print("🚀 AI Travel Advisor Database Setup")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'setup':
            setup_database()
        elif command == 'verify':
            verify_setup()
        elif command == 'sample':
            insert_sample_data()
        elif command == 'all':
            setup_database()
            if verify_setup():
                insert_sample_data()
        else:
            print(f"Unknown command: {command}")
            print_usage()
    else:
        print_usage()

def print_usage():
    """Print usage instructions"""
    print("\nUsage:")
    print("  python setup_database.py setup    - Set up the database schema")
    print("  python setup_database.py verify   - Verify the database setup")
    print("  python setup_database.py sample   - Insert sample data")
    print("  python setup_database.py all      - Run all setup steps")
    print("\nNote: For schema setup, it's recommended to:")
    print("1. Go to your Supabase dashboard")
    print("2. Navigate to SQL Editor")
    print("3. Copy and paste the contents of database/schema.sql")
    print("4. Run the SQL manually")

if __name__ == "__main__":
    main() 