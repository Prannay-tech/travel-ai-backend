#!/bin/bash

# 🌐 AI Travel Advisor - Final Pipeline Setup Script
# This script sets up the complete end-to-end pipeline

set -e

echo "🚀 Setting up AI Travel Advisor - Final Pipeline"
echo "================================================"

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

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is required but not installed"
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is required but not installed"
        exit 1
    fi
    
    print_success "All dependencies are installed"
}

# Setup environment variables
setup_environment() {
    print_status "Setting up environment variables..."
    
    if [ ! -f .env ]; then
        cat > .env << EOF
# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_service_role_key_here

# API Keys
OPENTRIPMAP_API_KEY=your_opentripmap_api_key_here
AMADEUS_API_KEY=your_amadeus_api_key_here

# Optional: Slack notifications
SLACK_WEBHOOK_URL=your_slack_webhook_url_here

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
EOF
        print_warning "Created .env file. Please update it with your actual API keys and configuration."
    else
        print_success ".env file already exists"
    fi
}

# Setup Python virtual environment
setup_python_env() {
    print_status "Setting up Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Created virtual environment"
    else
        print_success "Virtual environment already exists"
    fi
    
    source venv/bin/activate
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r backend/requirements.txt
    pip install sentence-transformers supabase pandas requests fastapi uvicorn
    
    print_success "Python dependencies installed"
}

# Setup database
setup_database() {
    print_status "Setting up Supabase database..."
    
    source venv/bin/activate
    
    # Check if environment variables are set
    if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ]; then
        print_warning "Supabase environment variables not set. Loading from .env file..."
        export $(cat .env | grep -v '^#' | xargs)
    fi
    
    if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ]; then
        print_error "Supabase credentials not found. Please update your .env file."
        exit 1
    fi
    
    # Run database setup
    python setup_database.py
    
    print_success "Database setup completed"
}

# Setup frontend
setup_frontend() {
    print_status "Setting up React frontend..."
    
    cd frontend
    
    # Install Node.js dependencies
    if [ ! -d "node_modules" ]; then
        npm install
        print_success "Frontend dependencies installed"
    else
        print_success "Frontend dependencies already installed"
    fi
    
    cd ..
}

# Run enhanced ETL pipeline
run_etl_pipeline() {
    print_status "Running enhanced ETL pipeline..."
    
    source venv/bin/activate
    
    # Load environment variables
    export $(cat .env | grep -v '^#' | xargs)
    
    # Run the enhanced ETL pipeline
    python etl/enhanced_etl_pipeline.py
    
    print_success "ETL pipeline completed"
}

# Start services
start_services() {
    print_status "Starting services..."
    
    # Start backend in background
    print_status "Starting FastAPI backend..."
    source venv/bin/activate
    export $(cat .env | grep -v '^#' | xargs)
    cd backend
    python main.py &
    BACKEND_PID=$!
    cd ..
    
    # Wait for backend to start
    sleep 5
    
    # Start frontend in background
    print_status "Starting React frontend..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    print_success "Services started successfully!"
    echo ""
    echo "🌐 Your AI Travel Advisor is now running!"
    echo "   Backend API: http://localhost:8000"
    echo "   Frontend UI: http://localhost:3000"
    echo "   API Documentation: http://localhost:8000/docs"
    echo ""
    echo "📋 Available endpoints:"
    echo "   GET /recommend - Get destination recommendations"
    echo "   GET /details/{id} - Get destination details"
    echo "   GET /flight-deal - Get flight deals"
    echo ""
    echo "🛑 To stop services, run: pkill -f 'python main.py' && pkill -f 'react-scripts'"
}

# Main setup function
main() {
    echo ""
    print_status "Starting AI Travel Advisor setup..."
    echo ""
    
    check_dependencies
    setup_environment
    setup_python_env
    setup_database
    setup_frontend
    
    echo ""
    print_status "Setup completed! Would you like to:"
    echo "1. Run the ETL pipeline to populate data"
    echo "2. Start the services (backend + frontend)"
    echo "3. Both"
    echo "4. Exit"
    echo ""
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            run_etl_pipeline
            ;;
        2)
            start_services
            ;;
        3)
            run_etl_pipeline
            start_services
            ;;
        4)
            print_success "Setup completed. You can run the services manually later."
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
}

# Run main function
main "$@" 