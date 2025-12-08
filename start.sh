#!/usr/bin/env bash

# Start the uMap Data API server
echo "Starting uMap Data API..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create data directory if it doesn't exist
mkdir -p data

# Copy example environment file if .env doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file from template"
fi

# Run the application
echo "Starting server on http://localhost:8000"
python main.py