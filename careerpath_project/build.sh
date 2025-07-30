#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Tesseract OCR and its dependencies
echo "Updating package lists..."
apt-get update

echo "Installing Tesseract OCR..."
apt-get install -y tesseract-ocr

echo "Installing Python dependencies..."
# Install Python libraries
pip install -r requirements.txt

echo "Build script finished."

