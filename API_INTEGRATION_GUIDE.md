# API Integration Guide for Travel AI

This guide covers all the APIs integrated into the Travel AI platform and how to set them up.

## 🔑 Required API Keys

### 1. **Groq AI API** (Required for AI Chat)
- **Purpose**: Powers the AI travel planning conversations
- **Get Key**: https://console.groq.com/
- **Cost**: Free tier available
- **Environment Variable**: `GROQ_API_KEY`

### 2. **Skyscanner API** (Optional - Flight Search)
- **Purpose**: Real flight search and pricing
- **Get Key**: https://www.partners.skyscanner.net/
- **Cost**: Free tier available
- **Environment Variable**: `SKYSCANNER_API_KEY`

### 3. **Hotels.com API** (Optional - Hotel Search)
- **Purpose**: Real hotel search and booking
- **Get Key**: https://rapidapi.com/hotels-com-provider/
- **Cost**: Free tier available
- **Environment Variable**: `HOTELS_API_KEY`

### 4. **WeatherAPI.com** (Optional - Weather Data)
- **Purpose**: Real-time weather information for destinations
- **Get Key**: https://www.weatherapi.com/
- **Cost**: Free tier available
- **Environment Variable**: `WEATHER_API_KEY`

### 5. **Google Places API** (Optional - Activities & POIs)
- **Purpose**: Tourist attractions and activities
- **Get Key**: https://developers.google.com/maps/documentation/places/web-service
- **Cost**: Free tier available
- **Environment Variable**: `GOOGLE_PLACES_API_KEY`

### 6. **Currency API** (Optional - Real-time Exchange Rates)
- **Purpose**: Real-time currency conversion
- **Get Key**: https://exchangerate.host/
- **Cost**: Free tier available
- **Environment Variable**: `CURRENCY_API_KEY`

## 🚀 Setup Instructions

### Step 1: Get API Keys
1. Visit each API provider's website
2. Sign up for a free account
3. Generate your API keys
4. Note down the keys securely

### Step 2: Configure Environment Variables

Create a `.env` file in the `clean_backend/` directory:

```bash
# Required
GROQ_API_KEY=your-groq-api-key-here

# Optional - Flight Search
SKYSCANNER_API_KEY=your-skyscanner-key-here

# Optional - Hotel Search
HOTELS_API_KEY=your-hotels-api-key-here

# Optional - Weather Data
WEATHER_API_KEY=your-weather-api-key-here

# Optional - Places & Activities
GOOGLE_PLACES_API_KEY=your-google-places-key-here

# Optional - Currency Conversion
CURRENCY_API_KEY=your-currency-api-key-here
```

### Step 3: Test API Connections

Run the backend and test each endpoint:

```bash
# Test health check
curl http://localhost:8000/health

# Test AI chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "conversation_history": []}'

# Test recommendations
curl -X POST http://localhost:8000/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "budget_per_person": "1000-2000",
    "people_count": "2 people",
    "travel_from": "New York",
    "travel_type": "international",
    "destination_type": "beach",
    "travel_dates": "next summer",
    "currency": "USD"
  }'
```

## 📊 API Endpoints

### Core Endpoints

| Endpoint | Method | Description | Required API Key |
|----------|--------|-------------|------------------|
| `/health` | GET | Health check | None |
| `/chat` | POST | AI conversation | Groq |
| `/recommendations` | POST | Travel recommendations | Groq |
| `/destinations` | GET | All destinations | None |

### Search Endpoints

| Endpoint | Method | Description | Required API Key |
|----------|--------|-------------|------------------|
| `/flights` | POST | Flight search | Skyscanner |
| `/hotels` | POST | Hotel search | Hotels.com |
| `/activities` | POST | Activity search | Google Places |

### Utility Endpoints

| Endpoint | Method | Description | Required API Key |
|----------|--------|-------------|------------------|
| `/currency/convert` | GET | Currency conversion | Currency API |

## 🔧 API Integration Details

### 1. **Groq AI Integration**
```python
# Backend implementation
async def call_groq_ai(message: str, conversation_history: List[Dict[str, str]] = None) -> str:
    messages = [{"role": "system", "content": AI_SYSTEM_PROMPT}]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": message})
    
    response = await client.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama3-70b-8192",
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 800
        }
    )
```

### 2. **Skyscanner Flight Search**
```python
# Backend implementation
async def get_real_flights(search: FlightSearch) -> List[Dict]:
    response = await client.get(
        "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create",
        headers={"x-api-key": SKYSCANNER_API_KEY},
        params={
            "origin": search.origin,
            "destination": search.destination,
            "date": search.departure_date,
            "adults": search.passengers
        }
    )
```

### 3. **Weather API Integration**
```python
# Backend implementation
async def get_weather_data(destination: str) -> Dict:
    response = await client.get(
        "http://api.weatherapi.com/v1/current.json",
        params={
            "key": WEATHER_API_KEY,
            "q": destination
        }
    )
```

## 🎯 Frontend Integration

### API Service Usage
```javascript
import { apiService } from './services/apiService';

// Chat with AI
const response = await apiService.chatWithAI("I want to go to Bali", history);

// Get recommendations
const recommendations = await apiService.getRecommendations(preferences);

// Search flights
const flights = await apiService.searchFlights({
  origin: "JFK",
  destination: "LAX",
  departure_date: "2024-06-15",
  passengers: 2
});
```

## 🔄 Fallback Strategy

The system uses a smart fallback strategy:

1. **Primary**: Real API data when keys are available
2. **Fallback**: High-quality mock data when APIs are unavailable
3. **Graceful Degradation**: System continues to work without optional APIs

### Mock Data Quality
- Realistic pricing and availability
- Accurate destination information
- Proper currency conversion
- Realistic flight/hotel options

## 📈 Performance Optimization

### Caching Strategy
```python
# Implement caching for expensive API calls
from functools import lru_cache
import time

@lru_cache(maxsize=100)
def get_cached_weather_data(destination: str, timestamp: int):
    # Cache weather data for 1 hour
    return get_weather_data(destination)
```

### Rate Limiting
```python
# Implement rate limiting for API calls
import asyncio
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_calls: int, time_window: int):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    async def acquire(self):
        now = datetime.now()
        self.calls = [call for call in self.calls if now - call < timedelta(seconds=self.time_window)]
        
        if len(self.calls) >= self.max_calls:
            await asyncio.sleep(1)
        
        self.calls.append(now)
```

## 🛡️ Security Best Practices

### API Key Management
1. **Never commit API keys to version control**
2. **Use environment variables**
3. **Rotate keys regularly**
4. **Monitor API usage**

### Error Handling
```python
try:
    response = await api_call()
    return response.data
except httpx.HTTPStatusError as e:
    logger.error(f"API Error: {e.response.status_code}")
    return fallback_data()
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return fallback_data()
```

## 📊 Monitoring & Analytics

### API Usage Tracking
```python
import logging
from datetime import datetime

def track_api_usage(api_name: str, endpoint: str, success: bool):
    logger.info(f"API Usage: {api_name}/{endpoint} - {'SUCCESS' if success else 'FAILED'}")
```

### Health Checks
```python
async def check_api_health():
    apis = {
        "groq": check_groq_health(),
        "skyscanner": check_skyscanner_health(),
        "weather": check_weather_health()
    }
    
    results = await asyncio.gather(*apis.values(), return_exceptions=True)
    return dict(zip(apis.keys(), results))
```

## 🚀 Deployment Considerations

### Environment Variables in Production
```bash
# Production environment variables
export GROQ_API_KEY=your-production-key
export SKYSCANNER_API_KEY=your-production-key
export WEATHER_API_KEY=your-production-key
```

### API Limits and Quotas
- Monitor API usage to stay within free tiers
- Implement caching to reduce API calls
- Use fallback data for non-critical features

## 📝 Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Verify the key is correct
   - Check if the key has expired
   - Ensure the key has proper permissions

2. **Rate Limiting**
   - Implement exponential backoff
   - Use caching to reduce API calls
   - Monitor usage patterns

3. **Network Issues**
   - Implement retry logic
   - Use fallback data
   - Log network errors for debugging

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test individual APIs
async def test_apis():
    print("Testing Groq AI...")
    await test_groq_ai()
    
    print("Testing Skyscanner...")
    await test_skyscanner()
    
    print("Testing Weather API...")
    await test_weather_api()
```

## 🎯 Next Steps

1. **Get API Keys**: Start with Groq AI (required)
2. **Test Integration**: Verify each API works
3. **Monitor Usage**: Track API calls and costs
4. **Optimize**: Implement caching and rate limiting
5. **Scale**: Add more APIs as needed

---

**Remember**: The system works perfectly with just the Groq AI key. All other APIs are optional enhancements!
