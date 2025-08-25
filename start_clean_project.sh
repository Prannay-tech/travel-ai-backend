#!/bin/bash

# Travel AI - Clean Project Startup Script
echo "🚀 Starting Travel AI - Clean Project"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Start Backend
echo "🔧 Starting Backend Server..."
cd clean_backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "📦 Installing backend dependencies..."
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔑 Creating .env file..."
    echo "GROQ_API_KEY=your-groq-api-key-here" > .env
    echo "⚠️  Please update the GROQ_API_KEY in clean_backend/.env with your actual key"
fi

# Start backend server in background
echo "🚀 Starting FastAPI server on http://localhost:8000"
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start Frontend
echo "🎨 Starting Frontend..."
cd ../clean_frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install > /dev/null 2>&1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔑 Creating frontend .env file..."
    echo "REACT_APP_GROQ_API_KEY=your-groq-api-key-here" > .env
    echo "REACT_APP_API_URL=http://localhost:8000" >> .env
fi

# Start frontend server
echo "🚀 Starting React app on http://localhost:3000"
npm start &
FRONTEND_PID=$!

echo ""
echo "🎉 Travel AI is starting up!"
echo "============================"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "💡 To get your Groq API key:"
echo "   1. Visit https://console.groq.com/"
echo "   2. Sign up for a free account"
echo "   3. Get your API key"
echo "   4. Update the .env files with your key"
echo ""
echo "🛑 To stop the servers, press Ctrl+C"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
