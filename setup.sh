#!/bin/bash
# Setup script for Network Diagram Tool on Ubuntu

echo "=========================================="
echo "Network Diagram Tool - Ubuntu Setup"
echo "=========================================="
echo ""

# Check if running on Ubuntu/Debian
if ! command -v apt-get &> /dev/null; then
    echo "❌ This script requires Ubuntu/Debian Linux"
    exit 1
fi

echo "📦 Updating package manager..."
sudo apt-get update -y

echo ""
echo "🐍 Installing Python 3 and pip..."
sudo apt-get install -y python3 python3-pip python3-dev

echo ""
echo "📚 Installing PyQt5 and dependencies..."
sudo apt-get install -y python3-pyqt5 python3-pyqt5.qtsvg python3-pyqt5.qtwebengine

echo ""
echo "📦 Installing Python packages from requirements.txt..."
pip3 install -r requirements.txt

echo ""
echo "=========================================="
echo "✅ Installation complete!"
echo "=========================================="
echo ""
echo "🚀 To run the application:"
echo "   python3 main.py"
echo ""
echo "📝 Project files will be saved in:"
echo "   ~/.ndt_projects/"
echo ""
