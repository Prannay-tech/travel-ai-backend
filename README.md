Travel AI Platform (Backend + Frontend)

Overview

This repository contains the FastAPI backend and a Next.js 14 frontend for an AI-powered travel planning platform. The system discovers destinations within a user’s budget and dates, estimates comprehensive costs (flights, hotels, daily expenses, transfers, insurance, visa), and presents curated itineraries with booking links.

Status

- Backend: Working with comprehensive cost calculation, dataset-driven cost of living, RapidAPI Skyscanner integration (rate-limits apply), currency conversion, weather, and AI (Groq) integration. API calls are currently throttled during local testing to avoid rate limits.
- Frontend: Live Next.js app with dark-mode UI, search with origin and date range, results list, destination detail page (photos, tabs, costs, hotels, restaurants, flights, info), and a floating chatbot UI.

Project Structure (Key Files)

- main.py: FastAPI app, endpoints, AI prompts, destination discovery, comprehensive cost calculation, RapidAPI endpoints (flights/hotels), and dataset integrations.
- flight_apis.py: Flight search abstraction for RapidAPI Skyscanner (web) and Amadeus with polling for incomplete searches and helpers to convert queries to place IDs.
- currency_api.py: Currency conversion via ExchangeRate-API with safe fallbacks.
- cost_of_living_dataset.py: Loads and serves daily cost components from the Kaggle CSV dataset, with helpers for lookups and fallbacks.
- weather_api.py: WeatherAPI.com integration for destination weather snapshots.
- travel-ai-frontend/: Next.js 14 app with TypeScript, Tailwind, Framer Motion, Zustand, React Query.
  - src/app/page.tsx: Landing page (dark mode, image carousel, hero search).
  - src/app/search/page.tsx: Search results with filters, sorting, and loading states.
  - src/app/destination/[id]/page.tsx: Destination detail page with gallery, tabs (Overview/Activities/Hotels/Restaurants/Flights/Info), and booking links.
  - src/components/SearchBar.tsx: Search inputs (query, origin, budget, date range, travelers, type).
  - src/components/ImageCarousel.tsx: High-quality rotating background images.
  - src/components/DestinationCard.tsx: Destination summary card UI.
  - src/components/HowItWorks.tsx: Onboarding steps.
  - src/components/TravelChat.tsx: Floating chatbot UI.
  - src/lib/api.ts: Frontend API service for backend calls.
  - src/hooks/useApi.ts: Data-fetching hooks.

Backend Highlights

- AI-led cost estimation: calculate_comprehensive_trip_cost combines flights, hotels, daily spend (meals/transport/activities/misc), airport transfers, insurance, and visa.
- Dataset integration: cost_of_living_dataset.py reads cost_of_living_dataset.csv and aggregates city-level daily costs with tuned “tourist” markups.
- RapidAPI Skyscanner: multiple endpoints supported (auto-complete, search-one-way/roundtrip/multi-city, price calendar, cheapest one-way, hotels search/auto-complete). Includes incomplete → polling flow where required.
- Currency and weather: ExchangeRate-API and WeatherAPI.com integrations with safe fallbacks.
- Mock fallbacks: Where live APIs rate-limit or fail, code gracefully falls back to deterministic estimates.

Frontend Highlights

- Modern dark mode UI with glassmorphism and smooth animations.
- Date range picker and origin input to improve flight pricing accuracy.
- Destination detail page with a rich, tabbed layout and image modal.
- Side chatbot UI to support itinerary customization flows.

Environment Variables

Create a .env at project root (Railway env vars recommended for prod):

- GROQ_API_KEY: Groq LLM key
- SKYSCANNER_API_KEY: RapidAPI Skyscanner key
- WEATHER_API_KEY: WeatherAPI.com key
- CURRENCY_API_URL: ExchangeRate-API full URL (e.g., https://v6.exchangerate-api.com/v6/<KEY>/latest/USD)
- Optional Amadeus keys if used

Local Development

Backend

1. python -m venv .venv && source .venv/bin/activate
2. pip install -r requirements.txt
3. uvicorn main:app --reload

Frontend

1. cd travel-ai-frontend
2. npm install
3. npm run dev

Testing Notes

- Avoid repeated live flight/hotel calls locally to prevent RapidAPI rate limits. Use fallback-friendly test flows or cached responses during development.

Future Work

- Authentication: user accounts, sessions, saved trips.
- Caching + rate-limit mitigation for flight/hotel endpoints.
- Booking deep links and affiliate integrations for flights/hotels/activities.
- Persist itineraries and preferences in a database.
- Expand activities and restaurant data sources; add Google Places details.
- Improve chatbot to fully orchestrate itinerary edits in real time.

Deployment

- Railway: Procfile/runtime.txt included. Configure env vars in Railway dashboard. Push main to deploy.

License

Proprietary – for project use.

# Travel AI Backend API

A FastAPI-powered backend for the Travel AI application, providing AI-powered travel planning with booking integration.

## 🚀 Features

- **AI Chat**: Groq LLM-powered travel planning conversations
- **Destination Recommendations**: AI-powered travel suggestions based on preferences
- **Flight Search**: Real-time flight data using Amadeus API
- **Weather Data**: Current weather and forecasts using WeatherAPI
- **Currency Conversion**: Real-time exchange rates using ExchangeRate API
- **Hotel Search**: Hotel recommendations and booking links
- **Activity Planning**: Tourist activities and itinerary suggestions

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Python**: 3.11.7
- **AI**: Groq LLM (llama3-70b-8192)
- **APIs**: Amadeus, WeatherAPI, ExchangeRate API
- **Deployment**: Railway

## 📋 Prerequisites

- Python 3.11+
- API Keys for:
  - Groq AI
  - Amadeus (Flight Search)
  - WeatherAPI
  - ExchangeRate API

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Prannay-tech/travel-ai-backend.git
cd travel-ai-backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file with your API keys:
```env
GROQ_API_KEY=your_groq_api_key
AMADEUS_CLIENT_ID=your_amadeus_client_id
AMADEUS_CLIENT_SECRET=your_amadeus_client_secret
WEATHER_API_KEY=your_weather_api_key
CURRENCY_API_KEY=your_currency_api_key
```

### 4. Run the Application
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Health Check
- `GET /health` - Check API status

### AI Chat
- `POST /chat` - AI-powered travel planning conversations

### Travel Recommendations
- `POST /recommendations` - Get AI-powered destination suggestions

### Flight Search
- `POST /flights` - Search for flights

### Weather Data
- `GET /weather/{location}` - Get current weather
- `GET /weather/{location}/forecast` - Get weather forecast

### Currency Conversion
- `GET /currency/convert` - Convert between currencies
- `GET /currency/rates` - Get exchange rates

### Hotels & Activities
- `POST /hotels` - Search for hotels
- `POST /activities` - Search for activities

## 🚀 Deployment

### Railway Deployment
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push to main branch

### Environment Variables for Railway
Make sure to set these in your Railway project:
- `GROQ_API_KEY`
- `AMADEUS_CLIENT_ID`
- `AMADEUS_CLIENT_SECRET`
- `WEATHER_API_KEY`
- `CURRENCY_API_KEY`

## 🧪 Testing

Run the test suite:
```bash
python -m pytest test_main.py -v
```

## 📝 License

This project is part of the Travel AI application.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request 