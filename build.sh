#!/bin/bash
echo "Starting build process..."

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create instance folder if it doesn't exist
mkdir -p instance

# Set permissions
chmod +x build.sh

echo "Build completed successfully!"