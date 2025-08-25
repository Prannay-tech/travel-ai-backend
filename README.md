# Travel AI - AI-Powered Travel Planning Platform

A modern, AI-powered travel planning platform that helps users discover destinations, book flights, hotels, and plan activities using natural language conversations.

## 🌟 Features

- **🤖 AI Chat Interface**: Natural language conversation with Groq LLM
- **🗺️ Smart Recommendations**: AI-powered destination suggestions
- **✈️ Flight Booking**: Integrated flight search and booking
- **🏨 Hotel Booking**: Hotel recommendations and booking links
- **🎯 Activity Planning**: Popular activities and itinerary planning
- **💱 Multi-Currency Support**: Support for USD, EUR, GBP, CAD, AUD
- **🌍 Domestic & International**: Support for both domestic and international travel
- **🎨 Modern Dark UI**: Beautiful dark theme with glass morphism effects

## 🏗️ Architecture

- **Frontend**: React.js with Tailwind CSS (Dark Theme)
- **Backend**: FastAPI (Python)
- **AI**: Groq LLM API
- **Styling**: Modern glass morphism with gradient effects

## 📁 Project Structure

```
travel-ai/
├── clean_frontend/          # React frontend with dark theme
├── clean_backend/           # FastAPI backend
├── start_clean_project.sh   # Startup script
├── README_CLEAN.md         # Detailed setup guide
├── PROJECT_COMPLETE.md     # Project completion summary
└── README.md              # This file
```

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd travel-ai
   ```

2. **Run the startup script**
   ```bash
   chmod +x start_clean_project.sh
   ./start_clean_project.sh
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🔑 Setup Requirements

### Groq API Key
To enable AI features, you need a Groq API key:
1. Sign up at https://console.groq.com/
2. Get your API key
3. Add it to `.env` files in both `clean_frontend/` and `clean_backend/`

## 🎯 User Journey

1. **Chat with AI**: Tell the AI about your travel preferences
2. **Get Recommendations**: Receive personalized destination suggestions
3. **Select Destination**: Choose from AI-recommended destinations
4. **Book Flights**: Browse and select flight options
5. **Book Hotels**: Find and book accommodations
6. **Plan Activities**: Discover and plan activities for your trip

## 🛠️ Tech Stack

- **Frontend**: React 18, Tailwind CSS, Lucide React Icons
- **Backend**: FastAPI, Pydantic, HTTPX
- **AI**: Groq LLM (Llama 3.1 70B)
- **Styling**: Glass morphism, gradient effects, dark theme
- **Deployment**: Ready for deployment on platforms like Render

## 📱 UI Features

- **Dark Theme**: Beautiful dark gradient background
- **Glass Morphism**: Translucent cards with blur effects
- **Gradient Accents**: Purple to blue gradient styling
- **Smooth Animations**: Hover effects and transitions
- **Responsive Design**: Works on all devices
- **Modern Typography**: Clean, readable text

## 🔧 Development

### Frontend Development
```bash
cd clean_frontend
npm install
npm start
```

### Backend Development
```bash
cd clean_backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📊 API Endpoints

- `POST /chat` - AI chat interface
- `POST /recommendations` - Get travel recommendations
- `GET /flights` - Search flights
- `GET /hotels` - Search hotels
- `GET /activities` - Search activities
- `GET /health` - Health check

## 🚀 Deployment

The project is ready for deployment:
- Frontend can be deployed to Vercel, Netlify, or similar
- Backend can be deployed to Render, Railway, or similar
- Environment variables need to be configured for production

## 📈 Future Enhancements

- Real flight/hotel booking APIs integration
- User accounts and trip history
- Social sharing features
- Mobile app development
- Advanced AI features

## 🤝 Contributing

This is a college project demonstrating modern web development with AI integration.

## 📄 License

This project is for educational purposes.

---

**Built with ❤️ using React, FastAPI, and Groq AI** 