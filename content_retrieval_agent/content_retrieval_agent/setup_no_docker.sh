#!/bin/bash

echo "🚀 Content Retrieval Agent - No Docker Setup"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies (No Docker needed!)..."
pip install --upgrade pip
pip install -r requirements_no_docker.txt

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
fi

# Run ingestion with SQLite
echo "📊 Ingesting sample data into SQLite..."
python ingestion_sqlite.py

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🎉 No Docker needed - everything runs locally with SQLite!"
echo ""
echo "Next steps:"
echo "1. Start the API: python api_sqlite.py"
echo "2. Visit: http://localhost:8000/docs"
echo "3. Test API: python test_api.py"
echo ""
echo "Your data is stored in: marketing_content.db"
echo ""
