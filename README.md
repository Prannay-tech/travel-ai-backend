# Travel AI - Smart Travel Recommendations

An AI-powered travel recommendation system that combines data from multiple sources to provide personalized travel suggestions, smart search capabilities, and comprehensive travel planning tools.

## 🚀 Features

- **AI-Powered Recommendations**: Get personalized travel suggestions based on your preferences
- **Smart Search**: Natural language search for places and flights with semantic understanding
- **Real-time Data**: Access up-to-date information from OpenTripMap and Skyscanner APIs
- **Vector Search**: Advanced similarity search using embeddings
- **Modern UI**: Beautiful, responsive React frontend with Tailwind CSS
- **FastAPI Backend**: High-performance API with automatic documentation

## 🏗️ Architecture

```
travel-ai/
├── etl/                    # Data pipeline
│   ├── fetch_opentripmap.py    # OpenTripMap API integration
│   ├── fetch_skyscanner.py     # Skyscanner API integration
│   ├── clean.py                # Data cleaning and preprocessing
│   ├── embed.py                # Embedding generation
│   ├── load_supabase.py        # Database loading
│   └── run.py                  # Full pipeline runner
├── backend/                # FastAPI application
│   ├── main.py                 # API endpoints
│   └── requirements.txt        # Python dependencies
├── frontend/               # React application
│   ├── src/                    # React components
│   ├── public/                 # Static assets
│   └── package.json            # Node.js dependencies
└── README.md               # This file
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Supabase**: PostgreSQL database with real-time capabilities
- **Sentence Transformers**: For generating embeddings
- **Pandas**: Data manipulation and analysis
- **Requests**: HTTP library for API calls

### Frontend
- **React**: UI library
- **React Query**: Data fetching and caching
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client

### Data Sources
- **OpenTripMap API**: Places and attractions data
- **Skyscanner API**: Flight information
- **Sentence Transformers**: Pre-trained models for embeddings

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Supabase account
- API keys for OpenTripMap and Skyscanner

### Backend Setup

1. Navigate to the backend directory:
```bash
cd travel-ai/backend
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
export SUPABASE_URL="your_supabase_url"
export SUPABASE_KEY="your_supabase_key"
export OPENTRIPMAP_API_KEY="your_opentripmap_key"
export SKYSCANNER_API_KEY="your_skyscanner_key"
```

5. Run the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd travel-ai/frontend
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

## 🔄 Data Pipeline

### Running the ETL Pipeline

1. Navigate to the ETL directory:
```bash
cd travel-ai/etl
```

2. Create a configuration file `config.json`:
```json
{
  "opentripmap_api_key": "your_key",
  "skyscanner_api_key": "your_key",
  "supabase_url": "your_url",
  "supabase_key": "your_key",
  "search_queries": ["Paris", "London", "New York"],
  "flight_routes": [
    {"origin": "JFK-sky", "destination": "LAX-sky"},
    {"origin": "LHR-sky", "destination": "CDG-sky"}
  ]
}
```

3. Run the full pipeline:
```bash
python run.py --mode full
```

Or run specific components:
```bash
python run.py --mode places    # Places only
python run.py --mode flights   # Flights only
```

## 🗄️ Database Setup

### Supabase Tables

Run the following SQL in your Supabase SQL editor:

```sql
-- Places table
CREATE TABLE IF NOT EXISTS places (
    id SERIAL PRIMARY KEY,
    place_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    type TEXT,
    categories TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    country TEXT,
    city TEXT,
    state TEXT,
    postcode TEXT,
    street TEXT,
    house_number TEXT,
    osm TEXT,
    wikidata TEXT,
    wikipedia TEXT,
    rate DECIMAL(3, 2),
    otm TEXT,
    sources JSONB,
    extent JSONB,
    url TEXT,
    image TEXT,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Flights table
CREATE TABLE IF NOT EXISTS flights (
    id SERIAL PRIMARY KEY,
    quote_id TEXT UNIQUE NOT NULL,
    min_price DECIMAL(10, 2),
    currency TEXT DEFAULT 'USD',
    direct BOOLEAN DEFAULT FALSE,
    outbound_leg JSONB,
    inbound_leg JSONB,
    origin_id TEXT,
    destination_id TEXT,
    departure_date DATE,
    carrier_ids TEXT,
    stops INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Embeddings table
CREATE TABLE IF NOT EXISTS embeddings (
    id SERIAL PRIMARY KEY,
    record_id TEXT NOT NULL,
    record_type TEXT NOT NULL,
    embedding JSONB NOT NULL,
    text_for_embedding TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🚀 API Endpoints

### Places
- `GET /places/popular` - Get popular places
- `POST /search/places` - Search places with semantic similarity
- `GET /places/{place_id}` - Get place details

### Flights
- `GET /flights/trending` - Get trending flight routes
- `POST /search/flights` - Search flights

### Recommendations
- `POST /recommendations` - Get AI-powered travel recommendations

### Health
- `GET /health` - Health check endpoint
- `GET /` - API information

## 🎯 Usage Examples

### Search for Places
```bash
curl -X POST "http://localhost:8000/search/places" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "art museums in Paris",
    "limit": 10,
    "min_rating": 7.0
  }'
```

### Get AI Recommendations
```bash
curl -X POST "http://localhost:8000/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "user_preferences": "I want to explore European cities with rich history",
    "budget": 3000,
    "duration": 7,
    "interests": ["Culture & History", "Food & Dining"]
  }'
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_KEY` | Supabase API key | Yes |
| `OPENTRIPMAP_API_KEY` | OpenTripMap API key | Yes |
| `SKYSCANNER_API_KEY` | Skyscanner API key | Yes |

### API Keys Setup

1. **OpenTripMap**: Sign up at [OpenTripMap](https://opentripmap.io/) and get your API key
2. **Skyscanner**: Sign up at [Skyscanner Partners](https://www.partners.skyscanner.net/) and get your API key
3. **Supabase**: Create a project at [Supabase](https://supabase.com/) and get your credentials

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenTripMap](https://opentripmap.io/) for places data
- [Skyscanner](https://www.skyscanner.net/) for flight data
- [Supabase](https://supabase.com/) for the database
- [Sentence Transformers](https://www.sbert.net/) for embeddings

## 📞 Support

For support, email support@travel-ai.com or create an issue in the repository. 