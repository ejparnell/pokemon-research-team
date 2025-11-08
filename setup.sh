#!/bin/bash

# Setup script for Pokémon Research Team project
echo "Setting up Pokémon Research Team environment..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete! To activate the environment, run:"
echo "source venv/bin/activate"