#!/bin/bash

# Django Stripe Payment Service - Quick Setup Script
# This script automates the initial project setup

echo "🚀 Django Stripe Payment Service - Setup Script"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create project directory structure
echo "📁 Creating project structure..."
mkdir -p payments/templates/payments
mkdir -p payments/static/payments
mkdir -p payments/management/commands
touch payments/management/__init__.py
touch payments/management/commands/__init__.py
echo "✓ Project structure created"
echo ""

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your Stripe keys:"
    echo "   1. Get keys from https://dashboard.stripe.com/test/apikeys"
    echo "   2. Add STRIPE_PUBLIC_KEY (starts with pk_test_)"
    echo "   3. Add STRIPE_SECRET_KEY (starts with sk_test_)"
    echo ""
    read -p "Press Enter after you've updated the .env file..."
else
    echo "✓ .env file already exists"
    echo ""
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations payments
python manage.py migrate
echo "✓ Migrations completed"
echo ""

# Create superuser
echo "👤 Creating superuser..."
echo "   Please enter admin credentials:"
python manage.py createsuperuser
echo "✓ Superuser created"
echo ""

# Create sample data
echo "📊 Creating sample data..."
python manage.py create_sample_data
echo "✓ Sample data created"
echo ""

# Collect static files
echo "📋 Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected"
echo ""

echo "✅ Setup complete!"
echo ""
echo "🎉 Your Django Stripe Payment Service is ready!"
echo ""
echo "Next steps:"
echo "1. Start the development server: python manage.py runserver"
echo "2. Visit http://localhost:8000"
echo "3. Access admin panel: http://localhost:8000/admin"
echo "4. Test a payment with card: 4242 4242 4242 4242"
echo ""
echo "For Docker deployment:"
echo "  docker-compose up --build"
echo ""
echo "Happy coding! 🚀"
