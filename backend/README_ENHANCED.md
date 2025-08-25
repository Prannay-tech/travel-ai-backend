# Enhanced Travel AI Backend

## Overview

The enhanced Travel AI backend provides a comprehensive API for travel recommendations with real-world data integration, including currency conversion, weather information, holiday data, and domestic/international travel options.

## Features

### 🌍 Real-World Data Integration
- **Currency Conversion**: Real-time exchange rates using Exchangerate.host API
- **Weather Data**: Current conditions and forecasts using WeatherAPI.com
- **Holiday Information**: Local festivals and national holidays using Calendarific API
- **Destination Database**: Curated domestic and international destinations with real pricing

### 💰 Currency Support
- **8 Major Currencies**: USD, EUR, GBP, JPY, CAD, AUD, CHF, SGD
- **Real-time Conversion**: Live exchange rates for accurate pricing
- **Budget Filtering**: Smart budget constraints in user's preferred currency

### 🏠 Domestic vs International Travel
- **Domestic Destinations**: US-focused locations with lower flight costs
- **International Destinations**: Global locations with visa and cultural information
- **Smart Filtering**: Different recommendations based on travel type

### 📊 Comprehensive Recommendations
- **Cost Analysis**: Daily costs + flight costs in selected currency
- **Weather Integration**: Current and forecasted weather for destinations
- **Holiday Calendar**: Local events and festivals during travel dates
- **Travel Tips**: Personalized advice based on preferences

## API Endpoints

### Core Recommendations
- `POST /recommendations/enhanced` - Get comprehensive travel recommendations
- `POST /recommendations` - Legacy endpoint (redirects to enhanced)

### Currency Services
- `POST /currency/convert` - Convert between currencies
- `GET /currency/rates` - Get current exchange rates
- `GET /currency/supported` - List supported currencies

### Weather Services
- `POST /weather/current` - Get current weather for location
- `POST /weather/forecast` - Get weather forecast
- `POST /weather/summary` - Get comprehensive weather summary

### Holiday Services
- `POST /holidays` - Get holidays for specific country/year
- `GET /holidays/upcoming` - Get upcoming holidays

### Destination Services
- `GET /destinations/domestic` - Get domestic US destinations
- `GET /destinations/international` - Get international destinations
- `GET /destinations/search` - Search destinations by criteria

### System
- `GET /` - API information and features
- `GET /health` - Health check with API key status

## Installation

### Prerequisites
- Python 3.8+
- pip
- Environment variables for API keys

### Setup

1. **Clone and navigate to backend directory**
```bash
cd backend
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Required
export SUPABASE_URL="your_supabase_url"
export SUPABASE_KEY="your_supabase_key"

# Optional (for enhanced features)
export WEATHER_API_KEY="your_weather_api_key"
export CALENDARIFIC_API_KEY="your_calendarific_api_key"
export TOMTOM_API_KEY="your_tomtom_api_key"
export AMADEUS_CLIENT_ID="your_amadeus_client_id"
export AMADEUS_CLIENT_SECRET="your_amadeus_client_secret"
```

4. **Run the enhanced backend**
```bash
python main_enhanced.py
```

Or using uvicorn directly:
```bash
uvicorn main_enhanced:app --host 0.0.0.0 --port 8000 --reload
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | Yes | Supabase project URL |
| `SUPABASE_KEY` | Yes | Supabase API key |
| `WEATHER_API_KEY` | No | WeatherAPI.com API key |
| `CALENDARIFIC_API_KEY` | No | Calendarific API key |
| `TOMTOM_API_KEY` | No | TomTom API key |
| `AMADEUS_CLIENT_ID` | No | Amadeus API client ID |
| `AMADEUS_CLIENT_SECRET` | No | Amadeus API client secret |
| `DEBUG` | No | Enable debug mode (default: False) |
| `LOG_LEVEL` | No | Logging level (default: INFO) |

### API Keys Setup

#### WeatherAPI.com
1. Sign up at [WeatherAPI.com](https://www.weatherapi.com/)
2. Get your API key from the dashboard
3. Set `WEATHER_API_KEY` environment variable

#### Calendarific
1. Sign up at [Calendarific](https://calendarific.com/)
2. Get your API key from the dashboard
3. Set `CALENDARIFIC_API_KEY` environment variable

#### Exchangerate.host (Currency)
- **API key required** - Sign up at [Exchangerate.host](https://exchangerate.host/)
- Set `EXCHANGERATE_API_KEY` environment variable

## Usage Examples

### Get Enhanced Recommendations

```python
import httpx

async def get_recommendations():
    async with httpx.AsyncClient() as client:
        data = {
            "destination": "beach",
            "budget": "5000",
            "travelDates": "summer 2024",
            "currentLocation": "New York",
            "preferences": "family-friendly, relaxing",
            "currency": "EUR",
            "travelType": "international"
        }
        
        response = await client.post(
            "http://localhost:8000/recommendations/enhanced",
            json=data
        )
        
        return response.json()
```

### Convert Currency

```python
async def convert_currency():
    async with httpx.AsyncClient() as client:
        data = {
            "amount": 1000.0,
            "from_currency": "USD",
            "to_currency": "EUR"
        }
        
        response = await client.post(
            "http://localhost:8000/currency/convert",
            json=data
        )
        
        return response.json()
```

### Get Weather Summary

```python
async def get_weather():
    async with httpx.AsyncClient() as client:
        data = {
            "location": "Tokyo, Japan",
            "days": 3
        }
        
        response = await client.post(
            "http://localhost:8000/weather/summary",
            json=data
        )
        
        return response.json()
```

## Testing

### Run Test Suite

```bash
python test_enhanced_api.py
```

### Manual Testing

1. **Start the server**
```bash
python main_enhanced.py
```

2. **Test health check**
```bash
curl http://localhost:8000/health
```

3. **Test currency conversion**
```bash
curl -X POST http://localhost:8000/currency/convert \
  -H "Content-Type: application/json" \
  -d '{"amount": 1000, "from_currency": "USD", "to_currency": "EUR"}'
```

4. **Test recommendations**
```bash
curl -X POST http://localhost:8000/recommendations/enhanced \
  -H "Content-Type: application/json" \
  -d '{"destination": "beach", "currency": "EUR", "travelType": "international"}'
```

## API Response Examples

### Enhanced Recommendations Response

```json
{
  "places": [
    {
      "name": "Bali, Indonesia",
      "country": "Indonesia",
      "description": "Tropical paradise with stunning beaches...",
      "image": "https://images.unsplash.com/...",
      "rating": 9.2,
      "cost_day_usd": 80,
      "cost_day_converted": 68,
      "flight_cost_converted": 1020,
      "currency": "EUR",
      "weather": "Tropical, 25-32°C year-round",
      "highlights": ["Beach resorts", "Cultural temples", "Rice terraces"],
      "best_time": "April to October",
      "airport": "DPS",
      "avg_flight_cost": 1200
    }
  ],
  "weather": {
    "location": {"name": "Bali", "country": "Indonesia"},
    "current": {
      "temperature": "30°C",
      "condition": "Partly Cloudy",
      "humidity": "80%"
    },
    "forecast": [
      {"day": "Today", "temp": "30°C", "condition": "Partly Cloudy"},
      {"day": "Tomorrow", "temp": "31°C", "condition": "Sunny"}
    ]
  },
  "holidays": [
    {
      "name": "Independence Day",
      "date": "2024-08-17",
      "description": "National independence celebration"
    }
  ],
  "summary": {
    "totalDestinations": 3,
    "averageCost": 68,
    "averageFlightCost": 1020,
    "bestTimeToVisit": "April to October for best weather",
    "travelTips": [
      "Book international flights 3-6 months in advance",
      "Pack sunscreen and beach essentials"
    ],
    "currency": "EUR",
    "travelType": "international"
  }
}
```

### Currency Conversion Response

```json
{
  "from_currency": "USD",
  "to_currency": "EUR",
  "amount": 1000.0,
  "converted_amount": 850.0,
  "rate": 0.85
}
```

## Architecture

### Directory Structure

```
backend/
├── main_enhanced.py          # Enhanced FastAPI application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── test_enhanced_api.py      # API test suite
├── clients/                  # External API clients
│   ├── __init__.py
│   ├── currency_client.py    # Currency conversion
│   ├── weather_client.py     # Weather data
│   └── holiday_client.py     # Holiday information
├── services/                 # Business logic services
│   ├── __init__.py
│   └── recommendation_service.py  # Main recommendation logic
└── README_ENHANCED.md        # This file
```

### Key Components

1. **Configuration (`config.py`)**
   - Environment variable management
   - API key validation
   - Settings for all services

2. **Clients (`clients/`)**
   - `CurrencyClient`: Exchangerate.host integration
   - `WeatherClient`: WeatherAPI.com integration
   - `HolidayClient`: Calendarific integration

3. **Services (`services/`)**
   - `RecommendationService`: Main business logic
   - Destination selection and filtering
   - Cost conversion and budget analysis

4. **API (`main_enhanced.py`)**
   - FastAPI application with enhanced endpoints
   - Request/response models
   - Error handling and validation

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input parameters
- **404 Not Found**: Data not available
- **500 Internal Server Error**: Server-side errors
- **503 Service Unavailable**: External API failures

All errors include descriptive messages and logging for debugging.

## Performance

### Caching
- Exchange rates cached for 1 hour
- Weather data cached for 30 minutes
- Holiday data cached for 24 hours

### Rate Limiting
- 60 requests per minute per IP
- Configurable via `RATE_LIMIT_PER_MINUTE`

### Async Operations
- All external API calls are asynchronous
- Concurrent processing for multiple data sources
- Non-blocking I/O operations

## Monitoring

### Health Check
The `/health` endpoint provides:
- Server status
- Database connectivity
- API key configuration status
- External service availability

### Logging
- Structured logging with different levels
- Request/response logging
- Error tracking and debugging
- Performance metrics

## Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main_enhanced:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup
```bash
# Production environment variables
export SUPABASE_URL="your_production_supabase_url"
export SUPABASE_KEY="your_production_supabase_key"
export WEATHER_API_KEY="your_weather_api_key"
export CALENDARIFIC_API_KEY="your_calendarific_api_key"
export DEBUG="False"
export LOG_LEVEL="INFO"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 