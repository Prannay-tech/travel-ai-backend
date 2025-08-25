#!/bin/bash

# AI Travel Advisor Database Quick Setup Script

echo "🚀 AI Travel Advisor Database Setup"
echo "=================================="

# Check if .env file exists
if [ ! -f "../.env" ]; then
    echo "❌ Error: .env file not found in project root"
    echo "Please create a .env file with your Supabase credentials:"
    echo "SUPABASE_URL=your_supabase_project_url"
    echo "SUPABASE_ANON_KEY=your_supabase_anon_key"
    echo "SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import supabase" 2>/dev/null || {
    echo "Installing supabase-py..."
    pip install supabase
}

python3 -c "import dotenv" 2>/dev/null || {
    echo "Installing python-dotenv..."
    pip install python-dotenv
}

echo "✅ Dependencies checked"

# Function to show menu
show_menu() {
    echo ""
    echo "Choose an option:"
    echo "1) Manual Setup (Recommended) - Copy SQL to Supabase dashboard"
    echo "2) Automated Setup - Run Python script"
    echo "3) Verify Database - Check if tables exist"
    echo "4) Insert Sample Data - Add test destinations"
    echo "5) Full Setup - Automated setup + verification + sample data"
    echo "6) Show Schema - Display the SQL schema"
    echo "7) Exit"
    echo ""
    read -p "Enter your choice (1-7): " choice
}

# Function to manual setup
manual_setup() {
    echo ""
    echo "📋 Manual Setup Instructions:"
    echo "1. Go to your Supabase dashboard"
    echo "2. Navigate to SQL Editor"
    echo "3. Copy the contents of database/schema.sql"
    echo "4. Paste and run the SQL"
    echo ""
    echo "Schema file location: $(pwd)/schema.sql"
    echo ""
    read -p "Press Enter to open the schema file..."
    
    if command -v code &> /dev/null; then
        code schema.sql
    elif command -v nano &> /dev/null; then
        nano schema.sql
    elif command -v vim &> /dev/null; then
        vim schema.sql
    else
        echo "Schema file: $(pwd)/schema.sql"
        cat schema.sql
    fi
}

# Function to automated setup
automated_setup() {
    echo ""
    echo "🤖 Running automated setup..."
    python3 setup_database.py setup
}

# Function to verify setup
verify_setup() {
    echo ""
    echo "🔍 Verifying database setup..."
    python3 setup_database.py verify
}

# Function to insert sample data
insert_sample_data() {
    echo ""
    echo "📝 Inserting sample data..."
    python3 setup_database.py sample
}

# Function to full setup
full_setup() {
    echo ""
    echo "🎯 Running full setup..."
    python3 setup_database.py all
}

# Function to show schema
show_schema() {
    echo ""
    echo "📄 Database Schema:"
    echo "=================="
    cat schema.sql
}

# Main menu loop
while true; do
    show_menu
    
    case $choice in
        1)
            manual_setup
            ;;
        2)
            automated_setup
            ;;
        3)
            verify_setup
            ;;
        4)
            insert_sample_data
            ;;
        5)
            full_setup
            ;;
        6)
            show_schema
            ;;
        7)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please enter a number between 1-7."
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done 