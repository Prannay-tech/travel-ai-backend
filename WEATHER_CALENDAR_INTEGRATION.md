# Weather and Calendar API Integration

## Overview
Successfully integrated **Weather API** (Open-Meteo) and **Calendarific API** (Holidays) into the Travel AI ETL pipeline alongside the existing TomTom POI API.

## What Was Implemented

### 1. Weather API Integration
- **Provider**: Open-Meteo (free, no API key required)
- **File**: `etl/weather_client.py`
- **Features**:
  - Current weather data (temperature, humidity, weather code)
  - 7-day weather forecast
  - Historical weather data
  - Automatic timezone detection

### 2. Calendarific API Integration
- **Provider**: Calendarific (API key: `bOuJMpGlgN6b8CNH1SdzwZXnkAi4qUQM`)
- **File**: `etl/calendarific_client.py`
- **Features**:
  - Holiday data for any country and year
  - Holiday types and descriptions
  - Date information in ISO format

### 3. Enhanced ETL Pipeline
- **File**: `etl/enhanced_etl_pipeline_with_weather_calendar.py`
- **Features**:
  - Fetches POIs from TomTom
  - Fetches weather data for each city
  - Fetches holidays for each country
  - Integrates all data sources into one pipeline

### 4. Test Scripts
- `etl/test_weather.py` - Tests weather API functionality
- `etl/test_calendarific.py` - Tests calendar API functionality
- `etl/test_data_fetching.py` - Tests all APIs together
- `etl/test_enhanced_pipeline.py` - Tests the full ETL pipeline

## API Test Results

✅ **All APIs working correctly:**
- **TomTom POI API**: Successfully fetching tourist attractions
- **Weather API**: Successfully fetching current weather and forecasts
- **Calendarific API**: Successfully fetching holidays for multiple countries

## Data Structure

### Weather Data
```json
{
  "city": "New York",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "current_temperature": 31.3,
  "current_humidity": 58,
  "current_weather_code": 0,
  "forecast_data": {...},
  "last_updated": "2024-01-15T10:30:00"
}
```

### Holiday Data
```json
{
  "name": "New Year's Day",
  "country": "US",
  "date": "2024-01-01",
  "type": "national",
  "description": "New Year's Day is the first day of the year",
  "year": 2024
}
```

## Next Steps

### 1. Supabase Schema Setup
You need to create the following tables in your Supabase project:

#### Weather Data Table
```sql
CREATE TABLE weather_data (
  id SERIAL PRIMARY KEY,
  city TEXT NOT NULL,
  latitude DECIMAL,
  longitude DECIMAL,
  current_temperature DECIMAL,
  current_humidity INTEGER,
  current_weather_code INTEGER,
  forecast_data JSONB,
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Holidays Table
```sql
CREATE TABLE holidays (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  country TEXT NOT NULL,
  date DATE NOT NULL,
  type TEXT,
  description TEXT,
  year INTEGER NOT NULL
);
```

### 2. Enable Supabase Integration
Once the tables are created, uncomment the Supabase insert lines in:
- `etl/enhanced_etl_pipeline_with_weather_calendar.py` (lines ~140 and ~155)

### 3. Run the Full Pipeline
```bash
python etl/test_enhanced_pipeline.py
```

### 4. Additional Features to Consider
- **Cost-of-living data** (Numbeo API)
- **Currency conversion** (Exchangerate.host)
- **Country information** (RESTCountries.com)
- **Historical weather patterns** for seasonal recommendations

## Usage Examples

### Fetch Weather for a City
```python
from weather_client import WeatherClient

weather = WeatherClient()
current = weather.get_current_weather(40.7128, -74.0060)  # New York
print(f"Temperature: {current['current']['temperature_2m']}°C")
```

### Fetch Holidays for a Country
```python
from calendarific_client import CalendarificClient

calendar = CalendarificClient()
holidays = calendar.get_holidays(country="US", year=2024)
print(f"Found {len(holidays)} holidays")
```

### Run Full ETL Pipeline
```python
from enhanced_etl_pipeline_with_weather_calendar import EnhancedETLPipelineWithWeatherCalendar

pipeline = EnhancedETLPipelineWithWeatherCalendar(supabase_url, supabase_key)
city_coords = [
    {'country': 'USA', 'lat': 40.7128, 'lon': -74.0060},
    {'country': 'France', 'lat': 48.8566, 'lon': 2.3522},
]
pipeline.run_pipeline(city_coords)
```

## Environment Variables
Make sure your `.env` file contains:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
TOMTOM_API_KEY=your_tomtom_key
CALENDARIFIC_API_KEY=bOuJMpGlgN6b8CNH1SdzwZXnkAi4qUQM
```

## Notes
- Weather API is free and doesn't require an API key
- Calendarific API has rate limits (check their documentation)
- All APIs are working correctly and tested
- The pipeline is ready to run once Supabase tables are created 