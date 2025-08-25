# Travel AI - Complete Setup Guide

This guide will walk you through setting up the complete Travel AI system following the 8-stage implementation plan.

## 🎯 Overview

The Travel AI system consists of:
- **Data Pipeline**: ETL processes for fetching and processing travel data
- **AI Backend**: FastAPI server with vector search capabilities
- **Frontend**: React application with modern UI
- **Database**: Supabase with pgvector for vector similarity search
- **Automation**: Scheduled ETL pipelines and monitoring

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- API keys for:
  - [OpenTripMap](https://opentripmap.io/) (free tier)
  - [RapidAPI Skyscanner](https://rapidapi.com/skyscanner/api/skyscanner-api/) (free tier)
  - [Supabase](https://supabase.com/) (free tier)

## 🚀 Stage-by-Stage Setup

### Stage 1: Data Ingestion

1. **Get API Keys**:
   ```bash
   # OpenTripMap API Key
   # Sign up at https://opentripmap.io/
   OPENTRIPMAP_API_KEY=your_key_here
   
   # Amadeus API Key
   # Sign up at https://developers.amadeus.com/
   AMADEUS_API_KEY=8W8ZGIcN61pNWmljxuc350cSGFUGXTCv
   ```

2. **Test Data Fetching**:
   ```bash
   cd travel-ai/etl
   
   # Test OpenTripMap
   python fetch_opentripmap.py
   
   # Test Amadeus API
   python fetch_amadeus.py
   ```

### Stage 2: Data Cleaning & Processing

1. **Install Enhanced Dependencies**:
   ```bash
   cd travel-ai/backend
   pip install -r requirements.txt
   
   # Download spaCy model
   python -m spacy download en_core_web_sm
   ```

2. **Test Enhanced Cleaning**:
   ```bash
   cd travel-ai/etl
   python enhanced_clean.py
   ```

### Stage 3: AI Embeddings

1. **Install Sentence Transformers**:
   ```bash
   pip install sentence-transformers
   ```

2. **Test Embedding Generation**:
   ```bash
   cd travel-ai/etl
   python embed.py
   ```

### Stage 4: Database & Vector Search

1. **Set up Supabase**:
   - Create account at [supabase.com](https://supabase.com/)
   - Create new project
   - Get your project URL and API key

2. **Enable pgvector Extension**:
   - Go to your Supabase dashboard
   - Navigate to SQL Editor
   - Run: `CREATE EXTENSION IF NOT EXISTS vector;`

3. **Set up Database Schema**:
   ```bash
   cd travel-ai
   
   # Set environment variables
   export SUPABASE_URL="your_supabase_url"
   export SUPABASE_KEY="your_supabase_key"
   
   # Run database setup
   python setup_database.py
   ```

4. **Test Vector Search**:
   ```bash
   cd travel-ai/etl
   python vector_search.py
   ```

### Stage 5: Backend API

1. **Set up Environment Variables**:
   ```bash
   cd travel-ai/backend
   
   # Create .env file
   cat > .env << EOF
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   OPENTRIPMAP_API_KEY=your_opentripmap_key
   RAPIDAPI_KEY=your_rapidapi_key
   EOF
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Backend Locally**:
   ```bash
   python main.py
   ```

4. **Test API Endpoints**:
   ```bash
   # Health check
   curl http://localhost:8000/health
   
   # Search places
   curl -X POST "http://localhost:8000/search/places" \
     -H "Content-Type: application/json" \
     -d '{"query": "art museums in Paris", "limit": 5}'
   ```

### Stage 6: Frontend Web UI

1. **Install Dependencies**:
   ```bash
   cd travel-ai/frontend
   npm install
   ```

2. **Configure API URL**:
   ```bash
   # Create .env file
   cat > .env << EOF
   REACT_APP_API_URL=http://localhost:8000
   EOF
   ```

3. **Run Frontend Locally**:
   ```bash
   npm start
   ```

4. **Build for Production**:
   ```bash
   npm run build
   ```

### Stage 7: Automation & Scheduling

1. **Set up Windsurf** (Alternative: GitHub Actions):
   ```bash
   # Install Windsurf CLI
   npm install -g @windsurf/cli
   
   # Deploy pipeline
   windsurf deploy -f windsurf.yaml
   ```

2. **Or Use GitHub Actions**:
   - Push code to GitHub
   - Actions will run automatically based on `.github/workflows/ci.yml`

### Stage 8: Monitoring & Uptime

1. **Set up UptimeRobot**:
   - Create account at [uptimerobot.com](https://uptimerobot.com/)
   - Import configuration from `monitoring/uptimerobot.json`
   - Update URLs with your actual deployment URLs

2. **Set up Render Monitoring**:
   - Deploy backend to Render using `render.yaml`
   - Monitor logs in Render dashboard

## 🌐 Deployment

### Backend Deployment (Render)

1. **Connect to Render**:
   - Push code to GitHub
   - Connect repository to Render
   - Use `render.yaml` for configuration

2. **Set Environment Variables in Render**:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `OPENTRIPMAP_API_KEY`
   - `AMADEUS_API_KEY`

### Frontend Deployment (GitHub Pages)

1. **Enable GitHub Pages**:
   - Go to repository settings
   - Enable GitHub Pages
   - Set source to `gh-pages` branch

2. **Update API URL**:
   - Set `REACT_APP_API_URL` to your Render backend URL

## 🔄 Running the Complete Pipeline

1. **Initial Data Load**:
   ```bash
   cd travel-ai/etl
   python run.py --mode full
   ```

2. **Daily Updates** (via Windsurf or cron):
   ```bash
   # Places only
   python run.py --mode places
   
   # Flights only
   python run.py --mode flights
   ```

## 🧪 Testing

1. **Backend Tests**:
   ```bash
   cd travel-ai/backend
   pytest tests/ -v
   ```

2. **Frontend Tests**:
   ```bash
   cd travel-ai/frontend
   npm test
   ```

3. **Integration Tests**:
   ```bash
   # Test complete flow
   curl -X POST "http://localhost:8000/recommendations" \
     -H "Content-Type: application/json" \
     -d '{
       "user_preferences": "I want to explore European cities with rich history",
       "budget": 3000,
       "duration": 7
     }'
   ```

## 📊 Monitoring & Logs

1. **Application Logs**:
   ```bash
   # Backend logs
   tail -f travel-ai/backend/logs/app.log
   
   # ETL logs
   tail -f travel-ai/etl/etl_pipeline.log
   ```

2. **Database Monitoring**:
   - Supabase dashboard
   - Query performance
   - Vector search metrics

3. **Uptime Monitoring**:
   - UptimeRobot dashboard
   - Response time tracking
   - Alert notifications

## 🔧 Troubleshooting

### Common Issues

1. **pgvector Extension Not Available**:
   ```sql
   -- Run in Supabase SQL Editor
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

2. **API Rate Limits**:
   - OpenTripMap: 1000 requests/day (free)
   - Amadeus: 1000 requests/month (free)
   - Implement caching for production

3. **Memory Issues with Embeddings**:
   - Use batch processing
   - Consider smaller models for production

4. **CORS Issues**:
   - Update CORS settings in `backend/main.py`
   - Ensure frontend URL is in allowed origins

### Performance Optimization

1. **Database Indexes**:
   - Ensure all indexes are created
   - Monitor query performance

2. **Caching**:
   - Implement Redis for API responses
   - Cache embeddings in memory

3. **Batch Processing**:
   - Process data in batches
   - Use async operations where possible

## 📈 Scaling Considerations

1. **Database Scaling**:
   - Upgrade Supabase plan for more resources
   - Consider dedicated PostgreSQL instance

2. **API Scaling**:
   - Use load balancers
   - Implement rate limiting
   - Add caching layers

3. **Data Pipeline Scaling**:
   - Use cloud functions for ETL
   - Implement streaming for real-time updates

## 🎉 Success Metrics

Monitor these key metrics:

- **API Response Time**: < 500ms
- **Uptime**: > 99.9%
- **Data Freshness**: Daily updates
- **Search Accuracy**: > 85% relevance
- **User Engagement**: Time on site, search queries

## 📞 Support

For issues and questions:
- Check the logs first
- Review this setup guide
- Create an issue in the repository
- Contact: support@travel-ai.com

---

**Congratulations!** You now have a complete, production-ready Travel AI system running on free tier services. The system will automatically fetch data, generate embeddings, provide AI-powered recommendations, and stay online with monitoring and alerts. 