#!/bin/bash

# Travel AI - Quick Start Script
# This script will set up the basic environment and run initial tests

set -e  # Exit on any error

echo "🚀 Travel AI - Quick Start Setup"
echo "================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3.8+ is required but not installed"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js $NODE_VERSION found"
else
    print_error "Node.js 16+ is required but not installed"
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    print_success "npm $NPM_VERSION found"
else
    print_error "npm is required but not installed"
    exit 1
fi

# Check Git
if command -v git &> /dev/null; then
    print_success "Git found"
else
    print_error "Git is required but not installed"
    exit 1
fi

print_success "All prerequisites met!"

# Create virtual environment
print_status "Setting up Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
print_success "Virtual environment created and activated"

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
print_status "Downloading spaCy model..."
python -m spacy download en_core_web_sm
print_success "Python dependencies installed"

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
cd ../frontend
npm install
print_success "Node.js dependencies installed"

# Create environment files
print_status "Creating environment files..."

# Backend .env
cd ../backend
if [ ! -f .env ]; then
    cat > .env << EOF
# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here

# API Keys
OPENTRIPMAP_API_KEY=your_opentripmap_key_here
AMADEUS_API_KEY=8W8ZGIcN61pNWmljxuc350cSGFUGXTCv

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
EOF
    print_warning "Created backend/.env - Please update with your API keys"
else
    print_status "backend/.env already exists"
fi

# Frontend .env
cd ../frontend
if [ ! -f .env ]; then
    cat > .env << EOF
REACT_APP_API_URL=http://localhost:8000
EOF
    print_success "Created frontend/.env"
else
    print_status "frontend/.env already exists"
fi

# Test installations
print_status "Testing installations..."

# Test Python packages
cd ../backend
source venv/bin/activate
python -c "import fastapi, pandas, numpy, sentence_transformers; print('✅ Python packages working')"

# Test Node.js packages
cd ../frontend
npm run build --silent
print_success "Frontend build successful"

# Create logs directory
cd ..
mkdir -p logs
print_success "Created logs directory"

# Display next steps
echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Update API keys in backend/.env:"
echo "   - Get OpenTripMap key: https://opentripmap.io/"
echo "   - Get RapidAPI key: https://rapidapi.com/skyscanner-api/"
echo "   - Get Supabase credentials: https://supabase.com/"
echo ""
echo "2. Set up Supabase database:"
echo "   python setup_database.py"
echo ""
echo "3. Start the backend:"
echo "   cd backend && source venv/bin/activate && python main.py"
echo ""
echo "4. Start the frontend (in new terminal):"
echo "   cd frontend && npm start"
echo ""
echo "5. Run the ETL pipeline:"
echo "   cd etl && python run.py --mode full"
echo ""
echo "📖 For detailed instructions, see SETUP_GUIDE.md"
echo ""

print_success "Quick start setup completed! 🚀" 