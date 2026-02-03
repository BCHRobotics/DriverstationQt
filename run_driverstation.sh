#!/bin/bash
# FRC Driver Station Launcher (Linux/macOS)

echo "FRC Driver Station - Setup and Launch"
echo "======================================"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Launch driver station
echo "Launching FRC Driver Station..."
python main.py "$@"
