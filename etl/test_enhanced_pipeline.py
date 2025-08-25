#!/usr/bin/env python3
"""
Test script for the enhanced ETL pipeline with weather and calendar integration.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_enhanced_pipeline():
    """Test the enhanced ETL pipeline."""
    try:
        from enhanced_etl_pipeline_with_weather_calendar import EnhancedETLPipelineWithWeatherCalendar
        
        # Check environment variables
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            print("❌ Missing Supabase credentials in environment variables")
            print("Please ensure SUPABASE_URL and SUPABASE_KEY are set in your .env file")
            return False
        
        print("✅ Environment variables loaded successfully")
        
        # Test with a smaller dataset first
        city_coords = [
            {'country': 'USA', 'lat': 40.7128, 'lon': -74.0060},   # New York
            {'country': 'France', 'lat': 48.8566, 'lon': 2.3522},  # Paris
        ]
        
        print("🚀 Starting enhanced ETL pipeline test...")
        pipeline = EnhancedETLPipelineWithWeatherCalendar(supabase_url, supabase_key)
        pipeline.run_pipeline(city_coords)
        
        print("✅ Enhanced ETL pipeline test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all required packages are installed")
        return False
    except Exception as e:
        print(f"❌ Error running enhanced ETL pipeline: {e}")
        return False

if __name__ == "__main__":
    success = test_enhanced_pipeline()
    sys.exit(0 if success else 1) 