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