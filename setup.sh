#!/bin/bash
# NovaFleet Inspection API - Quick Setup Script for macOS/Linux
# This script automates the initial setup process

echo "========================================"
echo "NovaFleet Inspection API Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/5] Python detected"
python3 --version
echo ""

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created successfully"
else
    echo "Virtual environment already exists"
fi
echo ""

# Activate virtual environment and install dependencies
echo "[3/5] Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
echo ""

# Run migrations
echo "[4/5] Setting up database..."
python manage.py makemigrations
python manage.py migrate
echo ""

# Setup complete
echo "[5/5] Setup complete!"
echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo ""
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Create a superuser (optional):"
echo "   python manage.py createsuperuser"
echo ""
echo "3. Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "4. Access the API:"
echo "   - API: http://localhost:8000/api/inspections"
echo "   - Swagger: http://localhost:8000/swagger/"
echo "   - Admin: http://localhost:8000/admin/"
echo ""
echo "5. Run tests:"
echo "   python manage.py test"
echo ""
echo "========================================"
