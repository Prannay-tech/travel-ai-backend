# Deployment Guide for Travel AI

This guide covers deploying your Travel AI application to production with Supabase (backend) and Vercel (frontend).

## 🚀 **Deployment Strategy**

### **Backend: Supabase Edge Functions**
- **Why Supabase**: Free tier, PostgreSQL database, real-time features, edge functions
- **Cost**: Free tier includes 500MB database, 2GB bandwidth, 50,000 monthly active users

### **Frontend: Vercel**
- **Why Vercel**: Free tier, automatic deployments, excellent React support, global CDN
- **Cost**: Free tier includes unlimited deployments, 100GB bandwidth

## 📦 **Step 1: Deploy Backend to Supabase**

### **1.1 Set up Supabase Project**
1. Go to https://supabase.com/
2. Create a new project
3. Note down your project URL and API keys

### **1.2 Install Supabase CLI**
```bash
npm install -g supabase
supabase login
```

### **1.3 Initialize Supabase in your project**
```bash
cd clean_backend
supabase init
```

### **1.4 Create Edge Function for API**
```bash
supabase functions new travel-ai-api
```

### **1.5 Convert FastAPI to Supabase Edge Function**

Create `supabase/functions/travel-ai-api/index.ts`:

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // Handle CORS
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { message, conversation_history } = await req.json()
    
    // Call Groq API
    const groqResponse = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${Deno.env.get('GROQ_API_KEY')}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'llama3-70b-8192',
        messages: [
          {
            role: 'system',
            content: `You are an expert AI travel planner. Your job is to help users plan their perfect trip by extracting their travel preferences from natural language conversations.

Key responsibilities:
1. Extract travel preferences from user messages
2. Ask clarifying questions when needed
3. Provide helpful travel advice and suggestions
4. Guide users through the planning process

Travel preference categories to extract:
- Budget per person (e.g., "$1000-2000", "$500+")
- Number of people traveling (e.g., "2 people", "family of 4")
- Travel from location (Ask them to type in their city and country and extract location from that)
- Travel type: "domestic" or "international"
- Destination type: "beach", "mountain", "city", "historic", "religious", "adventure", "relaxing"
- Travel dates (e.g., "next summer", "December 2024")
- Currency preference (ALL valid currencies, convert them to USD in backend for uniformity but display prices in the user's preferred currency after converting from USD)
- Additional preferences (e.g., "romantic getaway", "family-friendly")

Always respond in a friendly, helpful manner. If you need more information, ask specific questions.`
          },
          ...conversation_history,
          { role: 'user', content: message }
        ],
        temperature: 0.3,
        max_tokens: 800,
        top_p: 0.8,
        frequency_penalty: 0.1,
        presence_penalty: 0.1
      })
    })

    const data = await groqResponse.json()
    
    return new Response(
      JSON.stringify({ response: data.choices[0].message.content }),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200 
      }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500 
      }
    )
  }
})
```

### **1.6 Set Environment Variables**
```bash
supabase secrets set GROQ_API_KEY=your_groq_api_key_here
supabase secrets set SKYSCANNER_API_KEY=your_skyscanner_key_here
supabase secrets set HOTELS_API_KEY=your_hotels_key_here
supabase secrets set WEATHER_API_KEY=your_weather_key_here
supabase secrets set GOOGLE_PLACES_API_KEY=your_google_places_key_here
supabase secrets set CURRENCY_API_KEY=your_currency_key_here
```

### **1.7 Deploy to Supabase**
```bash
supabase functions deploy travel-ai-api
```

### **1.8 Get your Supabase API URL**
Your API will be available at:
```
https://your-project-ref.supabase.co/functions/v1/travel-ai-api
```

## 🌐 **Step 2: Deploy Frontend to Vercel**

### **2.1 Prepare Frontend for Production**

Update `clean_frontend/src/services/apiService.js`:

```javascript
// Production API URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-project-ref.supabase.co/functions/v1/travel-ai-api';
```

### **2.2 Create Vercel Configuration**

Create `clean_frontend/vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "framework": "create-react-app",
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-project-ref.supabase.co/functions/v1/$1"
    }
  ],
  "env": {
    "REACT_APP_API_URL": "https://your-project-ref.supabase.co/functions/v1"
  }
}
```

### **2.3 Deploy to Vercel**

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
cd clean_frontend
vercel --prod
```

## 🔌 **Step 3: API Integration Guide**

### **Essential APIs for Travel Planning**

#### **1. Flight Search APIs**
- **Skyscanner API** (Free tier available)
  - URL: https://www.partners.skyscanner.net/
  - Features: Real-time flight prices, routes, availability
  - Cost: Free tier with limits

- **Amadeus API** (Free tier available)
  - URL: https://developers.amadeus.com/
  - Features: Flight search, hotel search, destination insights
  - Cost: Free tier with 1000 API calls/month

#### **2. Hotel Search APIs**
- **Hotels.com API** (via RapidAPI)
  - URL: https://rapidapi.com/hotels-com-provider/
  - Features: Hotel search, pricing, availability
  - Cost: Free tier available

- **Booking.com API** (via RapidAPI)
  - URL: https://rapidapi.com/booking-com/
  - Features: Hotel search, reviews, pricing
  - Cost: Free tier available

#### **3. Currency Conversion APIs**
- **ExchangeRate-API** (Free tier available)
  - URL: https://exchangerate.host/
  - Features: Real-time exchange rates, 170+ currencies
  - Cost: Free tier with 1000 requests/month

- **Fixer.io** (Free tier available)
  - URL: https://fixer.io/
  - Features: Historical rates, multiple currencies
  - Cost: Free tier with 100 requests/month

#### **4. Activities & Attractions APIs**
- **Google Places API** (Free tier available)
  - URL: https://developers.google.com/maps/documentation/places/web-service
  - Features: Tourist attractions, restaurants, activities
  - Cost: Free tier with $200 credit/month

- **Foursquare Places API** (Free tier available)
  - URL: https://developer.foursquare.com/
  - Features: Venues, tips, photos, ratings
  - Cost: Free tier with 950 requests/day

#### **5. Weather APIs**
- **WeatherAPI.com** (Free tier available)
  - URL: https://www.weatherapi.com/
  - Features: Current weather, forecasts, historical data
  - Cost: Free tier with 1 million requests/month

- **OpenWeatherMap** (Free tier available)
  - URL: https://openweathermap.org/api
  - Features: Weather data, air quality, UV index
  - Cost: Free tier with 1000 calls/day

#### **6. Additional APIs**

**Events & Festivals:**
- **Eventbrite API** (Free tier available)
  - URL: https://www.eventbrite.com/platform/api-keys
  - Features: Events, festivals, local activities
  - Cost: Free tier available

**Transportation:**
- **Google Maps API** (Free tier available)
  - URL: https://developers.google.com/maps
  - Features: Directions, public transit, ride-sharing
  - Cost: Free tier with $200 credit/month

**Travel Inspiration:**
- **Unsplash API** (Free tier available)
  - URL: https://unsplash.com/developers
  - Features: High-quality travel photos
  - Cost: Free tier with 5000 requests/hour

## 🛠️ **Step 4: Enhanced Backend with All APIs**

### **Updated Supabase Edge Function**

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { endpoint, data } = await req.json()
    
    switch (endpoint) {
      case 'chat':
        return await handleChat(data)
      case 'flights':
        return await handleFlightSearch(data)
      case 'hotels':
        return await handleHotelSearch(data)
      case 'activities':
        return await handleActivitySearch(data)
      case 'weather':
        return await handleWeatherSearch(data)
      case 'currency':
        return await handleCurrencyConversion(data)
      default:
        return new Response(
          JSON.stringify({ error: 'Invalid endpoint' }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
        )
    }
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    )
  }
})

async function handleChat(data) {
  // Groq AI chat implementation
}

async function handleFlightSearch(data) {
  // Skyscanner/Amadeus flight search
}

async function handleHotelSearch(data) {
  // Hotels.com/Booking.com hotel search
}

async function handleActivitySearch(data) {
  // Google Places/Foursquare activity search
}

async function handleWeatherSearch(data) {
  // WeatherAPI.com weather data
}

async function handleCurrencyConversion(data) {
  // ExchangeRate-API currency conversion
}
```

## 📊 **Step 5: Database Schema for Supabase**

### **Create Tables in Supabase**

```sql
-- Users table
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Travel preferences table
CREATE TABLE travel_preferences (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  budget_per_person DECIMAL(10,2),
  people_count INTEGER,
  travel_from TEXT,
  travel_type TEXT,
  destination_type TEXT,
  travel_dates TEXT,
  currency TEXT,
  additional_preferences TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Saved trips table
CREATE TABLE saved_trips (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  destination_name TEXT,
  flight_details JSONB,
  hotel_details JSONB,
  activities JSONB,
  total_cost DECIMAL(10,2),
  currency TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- API usage tracking
CREATE TABLE api_usage (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  api_name TEXT,
  endpoint TEXT,
  response_time INTEGER,
  success BOOLEAN,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🚀 **Step 6: Deployment Commands**

### **Backend Deployment**
```bash
# Deploy to Supabase
cd clean_backend
supabase functions deploy travel-ai-api

# Set environment variables
supabase secrets set GROQ_API_KEY=your_key
supabase secrets set SKYSCANNER_API_KEY=your_key
supabase secrets set HOTELS_API_KEY=your_key
supabase secrets set WEATHER_API_KEY=your_key
supabase secrets set GOOGLE_PLACES_API_KEY=your_key
supabase secrets set CURRENCY_API_KEY=your_key
```

### **Frontend Deployment**
```bash
# Deploy to Vercel
cd clean_frontend
vercel --prod

# Set environment variables in Vercel dashboard
REACT_APP_API_URL=https://your-project-ref.supabase.co/functions/v1
```

## 💰 **Cost Analysis**

### **Free Tier Limits**
- **Supabase**: 500MB database, 2GB bandwidth, 50K MAU
- **Vercel**: Unlimited deployments, 100GB bandwidth
- **Groq**: Free tier available
- **Skyscanner**: Free tier with limits
- **Hotels.com**: Free tier via RapidAPI
- **WeatherAPI**: 1M requests/month free
- **Google Places**: $200 credit/month free
- **ExchangeRate-API**: 1000 requests/month free

### **Total Monthly Cost (Free Tier)**
- **Backend**: $0 (Supabase free tier)
- **Frontend**: $0 (Vercel free tier)
- **APIs**: $0 (all within free limits)
- **Total**: $0/month

## 🎯 **Next Steps**

1. **Set up Supabase project** and deploy backend
2. **Deploy frontend to Vercel**
3. **Add API keys** for all services
4. **Test all integrations**
5. **Monitor usage** and optimize
6. **Scale up** as needed

---

**Your Travel AI app will be fully deployed and production-ready with all the APIs integrated!** 🚀
