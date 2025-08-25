# Travel AI - Complete Travel Planning Platform

A comprehensive AI-powered travel planning and booking platform that helps users plan their perfect trips from start to finish.

## 🚀 Features

### AI-Powered Travel Planning
- **Intelligent Chat Interface**: Natural language conversation with AI to understand travel preferences
- **Smart Recommendations**: AI suggests destinations based on budget, preferences, and travel style
- **Personalized Experience**: Tailored recommendations for each user

### Complete Booking Workflow
1. **AI Chat**: Tell the AI your preferences (budget, destination type, travel dates, etc.)
2. **Destination Selection**: Choose from AI-recommended destinations
3. **Flight Booking**: Search and book flights with real-time data
4. **Hotel Booking**: Find and book accommodations
5. **Activity Planning**: Plan your itinerary with local activities and experiences

### Key Features
- **Multi-Currency Support**: USD, EUR, GBP, CAD, AUD, and more
- **Real-time Pricing**: Live flight and hotel prices
- **Comprehensive Data**: 20+ destinations with detailed information
- **Modern UI**: Beautiful, responsive design with Tailwind CSS
- **Complete Workflow**: End-to-end travel planning experience

## 🏗️ Architecture

```
Travel AI Platform
├── clean_backend/          # FastAPI Backend
│   ├── main.py            # Main API server
│   └── requirements.txt   # Python dependencies
├── clean_frontend/        # React Frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   └── App.js         # Main app component
│   └── package.json       # Node.js dependencies
└── README_CLEAN.md        # This file
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Groq AI**: LLM integration for intelligent conversations
- **HTTPX**: Async HTTP client for API calls
- **Pydantic**: Data validation and serialization

### Frontend
- **React**: UI library
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client

### AI & APIs
- **Groq LLM**: AI-powered travel planning
- **Mock Flight APIs**: Flight search and booking
- **Mock Hotel APIs**: Hotel search and booking
- **Activity APIs**: Local experiences and tours

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Groq API key (free at https://console.groq.com/)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd clean_backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file
echo "GROQ_API_KEY=your-groq-api-key-here" > .env
```

5. Run the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd clean_frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The React app will be available at `http://localhost:3000`

## 🎯 Usage Guide

### 1. Start Planning
- Visit the homepage and click "Start Planning"
- Or go directly to `/chat` to begin the AI conversation

### 2. AI Chat Interface
- Answer the AI's questions about your travel preferences:
  - Budget per person
  - Number of travelers
  - Travel from location
  - Domestic or international
  - Destination type (beach, mountain, city, etc.)
  - Travel dates
  - Currency preference
  - Additional preferences

### 3. Destination Selection
- Review AI-recommended destinations
- See pricing, ratings, and highlights
- Select your preferred destination

### 4. Flight Booking
- Browse available flights
- Compare prices and schedules
- Select your preferred flight

### 5. Hotel Booking
- Search for accommodations
- Filter by amenities and location
- Choose your hotel

### 6. Activity Planning
- Browse local activities and experiences
- Add activities to your itinerary
- Complete your trip planning

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `POST /chat` - AI conversation
- `POST /recommendations` - Get travel recommendations
- `POST /flights` - Search flights
- `POST /hotels` - Search hotels
- `POST /activities` - Get activities
- `GET /destinations` - All destinations
- `GET /currencies` - Supported currencies

### Example API Calls

#### Chat with AI
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want a beach vacation for 2 people with $2000 budget",
    "conversation_history": []
  }'
```

#### Get Recommendations
```bash
curl -X POST "http://localhost:8000/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "budget_per_person": "$1000-2000",
    "people_count": "2 people",
    "travel_from": "New York",
    "travel_type": "international",
    "destination_type": "beach",
    "currency": "USD"
  }'
```

## 🎨 UI Components

### Chat Interface
- Real-time AI conversation
- Suggestion buttons for easy selection
- Typing indicators
- Message history

### Destination Cards
- Beautiful destination images
- Pricing information
- Ratings and highlights
- Interactive selection

### Booking Interfaces
- Flight search with filters
- Hotel comparison
- Activity selection
- Progress tracking

## 🔒 Environment Variables

### Backend (.env)
```bash
GROQ_API_KEY=your-groq-api-key-here
SKYSCANNER_API_KEY=your-skyscanner-key
AMADEUS_CLIENT_ID=your-amadeus-client-id
AMADEUS_CLIENT_SECRET=your-amadeus-secret
```

### Frontend (.env)
```bash
REACT_APP_GROQ_API_KEY=your-groq-api-key-here
REACT_APP_API_URL=http://localhost:8000
```

## 🚀 Deployment

### Backend Deployment
The backend is ready for deployment on:
- **Render**: Use the provided `render.yaml`
- **Railway**: Direct deployment from GitHub
- **Heroku**: Add Procfile and deploy
- **Vercel**: Serverless deployment

### Frontend Deployment
The frontend can be deployed on:
- **Vercel**: Automatic deployment from GitHub
- **Netlify**: Drag and drop deployment
- **GitHub Pages**: Static hosting

## 🧪 Testing

### Backend Testing
```bash
cd clean_backend
python -m pytest
```

### Frontend Testing
```bash
cd clean_frontend
npm test
```

## 📊 Data Sources

### Destinations
- **Domestic**: Miami Beach, San Diego, Denver, New York, Chicago, Boston
- **International**: Bali, Maldives, Swiss Alps, Tokyo, Paris, Rome, Athens, Varanasi

### Features per Destination
- Detailed descriptions
- Pricing information
- Ratings and reviews
- Highlights and attractions
- Best times to visit
- Airport codes
- Available activities

## 🔮 Future Enhancements

### Planned Features
- **Real API Integration**: Connect to actual flight and hotel APIs
- **User Accounts**: Save preferences and travel history
- **Payment Processing**: Integrated booking and payment
- **Mobile App**: React Native mobile application
- **Multi-language Support**: Internationalization
- **Advanced AI**: More sophisticated travel recommendations

### API Integrations
- **Skyscanner**: Real flight data
- **Booking.com**: Hotel availability
- **Viator**: Activity bookings
- **Weather APIs**: Real-time weather data
- **Currency APIs**: Live exchange rates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Groq**: For providing fast, reliable AI models
- **Unsplash**: For beautiful destination images
- **Tailwind CSS**: For the amazing utility-first CSS framework
- **Lucide**: For the beautiful icon set

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API endpoints

---

**Ready to start your AI-powered travel planning journey?** 🚀✈️
