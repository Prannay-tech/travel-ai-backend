#!/bin/bash

# Travel AI - Complete Startup Script
# This script sets up and runs the entire Travel AI project

set -e  # Exit on any error

echo "🚀 Starting Travel AI Project Setup..."

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

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the travel-ai project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating template..."
    cat > .env << 'ENVEOF'
# API Keys
AMADEUS_CLIENT_ID=your_amadeus_client_id_here
AMADEUS_CLIENT_SECRET=your_amadeus_client_secret_here
OPENTRIPMAP_API_KEY=your_opentripmap_api_key_here

# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# Database Configuration
DATABASE_URL=your_database_url_here

# Application Configuration
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# Hugging Face Configuration
HF_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
ENVEOF
    print_warning "Please update the .env file with your actual API keys and credentials"
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# Install spaCy model
print_status "Installing spaCy language model..."
python -m spacy download en_core_web_sm

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_warning "Node.js not found. Installing via Homebrew..."
    if ! command -v brew &> /dev/null; then
        print_error "Homebrew not found. Please install Homebrew first: https://brew.sh/"
        exit 1
    fi
    brew install node
fi

# Install frontend dependencies
print_status "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p logs

print_success "Setup complete! 🎉"

echo ""
echo "📋 Next Steps:"
echo "1. Update the .env file with your API keys:"
echo "   - AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET"
echo "   - OPENTRIPMAP_API_KEY"
echo "   - SUPABASE_URL and SUPABASE_KEY"
echo ""
echo "2. Run the ETL pipeline:"
echo "   python etl/run_pipeline.py"
echo ""
echo "3. Start the backend server:"
echo "   cd backend && uvicorn main:app --reload"
echo ""
echo "4. Start the frontend development server:"
echo "   cd frontend && npm start"
echo ""
echo "5. Or use the quick start script:"
echo "   ./quick_start.sh"
echo ""

print_success "Travel AI project is ready to use!"
