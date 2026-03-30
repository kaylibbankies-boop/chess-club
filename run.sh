#!/bin/bash

# Chess Club Flask App Startup Script for macOS/Linux

echo ""
echo "============================================"
echo "  Chess Club Flask Application"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Installing dependencies..."
pip install -r requirements.txt --quiet

echo "[4/5] Checking configuration..."
if [ ! -f ".env" ]; then
    echo "Copying .env.example to .env"
    cp .env.example .env
fi

echo "[5/5] Starting Flask server..."
echo ""
echo "============================================"
echo "Server starting at: http://localhost:5000"
echo "Press Ctrl+C to stop"
echo "============================================"
echo ""

python3 app.py
