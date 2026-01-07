# Django Stripe Payment Service

A production-ready Django application that integrates with Stripe for processing payments. Supports individual item purchases and order-based purchases with discounts and taxes.

## 🚀 Features

### Core Features
- ✅ **Item Model** - Store items with name, description, price, and currency
- ✅ **Stripe Checkout Integration** - Secure payment processing via Stripe
- ✅ **API Endpoints** - RESTful endpoints for creating checkout sessions
- ✅ **Responsive UI** - Beautiful, modern interface for item browsing and purchasing

### Bonus Features
- ✅ **Docker Support** - Complete containerization with Docker Compose
- ✅ **Environment Variables** - Secure configuration management
- ✅ **Django Admin** - Full admin panel with custom configurations
- ✅ **Order System** - Bundle multiple items in a single order
- ✅ **Discount System** - Apply percentage or fixed-amount discounts
- ✅ **Tax System** - Add taxes to orders
- ✅ **Multi-Currency** - Support for USD and EUR

## 🛠 Tech Stack

- **Backend:** Django 4.2.9, Python 3.11
- **Payment:** Stripe API
- **Database:** PostgreSQL (production), SQLite (development)
- **Deployment:** Docker, Gunicorn, Whitenoise
- **Styling:** Pure CSS (no frameworks)

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose (for containerized setup)
- Stripe Account (get test keys from https://stripe.com)

## 🚀 Quick Start

### Option 1: Docker Setup (Recommended)

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd django-stripe-payment
```

2. **Create environment file**
```bash
cp .env.example .env
```

3. **Edit `.env` file with your credentials**
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
DATABASE_URL=postgresql://postgres:postgres@db:5432/stripe_payments
ALLOWED_HOSTS=localhost,127.0.0.1
```

4. **Build and run with Docker**
```bash
docker-compose up --build
```

5. **Create superuser (in another terminal)**
```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Access the application**
- Main site: http://localhost:8000
- Admin panel: http://localhost:8000/admin

### Option 2: Local Development Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd django-stripe-payment
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic
```

8. **Run development server**
```bash
python manage.py runserver
```

## 📚 API Documentation

### Endpoints

#### 1. Get Item Page
```
GET /item/{id}/
```
Returns HTML page displaying item details with a "Buy" button.

**Example:**
```bash
curl http://localhost:8000/item/1/
```

#### 2. Create Checkout Session for Item
```
GET /buy/{id}/
```
Creates a Stripe Checkout Session for the specified item.

**Response:**
```json
{
  "id": "cs_test_a1b2c3d4..."
}
```

**Example:**
```bash
curl http://localhost:8000/buy/1/
```

#### 3. Get Order Page
```
GET /order/{id}/
```
Returns HTML page displaying order details with all items, discounts, and taxes.

#### 4. Create Checkout Session for Order
```
GET /buy/order/{id}/
```
Creates a Stripe Checkout Session for the specified order.

**Response:**
```json
{
  "id": "cs_test_a1b2c3d4..."
}
```

## 🎨 Usage Guide

### Adding Items

1. Go to admin panel: http://localhost:8000/admin
2. Navigate to "Items"
3. Click "Add Item"
4. Fill in:
   - Name: Product name
   - Description: Product description
   - Price: Price in decimal format (e.g., 29.99)
   - Currency: Select USD or EUR
5. Click "Save"

### Creating Orders

1. In admin panel, go to "Orders"
2. Click "Add Order"
3. Select multiple items
4. (Optional) Add a discount
5. (Optional) Add a tax
6. Click "Save"

### Adding Discounts

1. Go to "Discounts" in admin
2. Click "Add Discount"
3. Fill in:
   - Name: Display name
   - Code: Unique discount code
   - Type: Percentage or Fixed Amount
   - Value: Discount value
   - Active: Check to enable
4. Click "Save"

### Adding Taxes

1. Go to "Taxes" in admin
2. Click "Add Tax"
3. Fill in:
   - Name: Tax name (e.g., "VAT")
   - Rate: Percentage (e.g., 20 for 20%)
   - Country: ISO country code (e.g., "US")
   - Active: Check to enable
4. Click "Save"

## 🧪 Testing Payments

Use Stripe's test card numbers:

- **Success:** 4242 4242 4242 4242
- **Decline:** 4000 0000 0000 0002
- **Requires Auth:** 4000 0027 6000 3184

Use any future expiry date, any 3-digit CVC, and any billing postal code.

## 🌐 Deployment

### Deploying to Railway

1. **Create Railway account** at https://railway.app

2. **Install Railway CLI**
```bash
npm i -g @railway/cli
```

3. **Login and initialize**
```bash
railway login
railway init
```

4. **Add PostgreSQL**
```bash
railway add --database postgresql
```

5. **Set environment variables**
```bash
railway variables set SECRET_KEY="your-secret-key"
railway variables set STRIPE_PUBLIC_KEY="pk_test_..."
railway variables set STRIPE_SECRET_KEY="sk_test_..."
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS="your-app.railway.app"
```

6. **Deploy**
```bash
railway up
```

7. **Run migrations**
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

### Deploying to Render

1. Create account at https://render.com
2. Create new Web Service
3. Connect your GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn config.wsgi:application`
5. Add environment variables in Render dashboard
6. Add PostgreSQL database
7. Deploy

## 📁 Project Structure

```
django-stripe-payment/
├── config/                 # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── payments/              # Main application
│   ├── models.py          # Data models (Item, Order, Discount, Tax)
│   ├── views.py           # View functions
│   ├── admin.py           # Admin configuration
│   ├── urls.py            # App URL patterns
│   └── templates/         # HTML templates
│       └── payments/
│           ├── home.html
│           ├── item_detail.html
│           ├── order_detail.html
│           ├── success.html
│           └── cancel.html
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker image definition
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
└── README.md             # This file
```

## 🔒 Security Notes

- Never commit `.env` file to version control
- Always use environment variables for sensitive data
- Use strong `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Keep Stripe keys secure
- Use HTTPS in production

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart services
docker-compose restart
```

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Or with Docker
docker-compose exec web python manage.py collectstatic --noinput
```

### Stripe Errors
- Verify API keys are correct in `.env`
- Check that keys match the environment (test vs live)
- Ensure Stripe webhook endpoints are configured (if using webhooks)

## 📝 Environment Variables Reference

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | Yes | `django-insecure-xyz123` |
| `DEBUG` | Debug mode flag | Yes | `True` or `False` |
| `STRIPE_PUBLIC_KEY` | Stripe publishable key | Yes | `pk_test_abc123` |
| `STRIPE_SECRET_KEY` | Stripe secret key | Yes | `sk_test_def456` |
| `DATABASE_URL` | PostgreSQL connection string | No | `postgresql://user:pass@host:5432/db` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | Yes | `localhost,example.com` |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for CSRF | No | `https://example.com` |

## 📄 License

This project is for educational purposes as part of a technical assessment.

## 👤 Author

Your Name - Technical Assessment Submission

## 🙏 Acknowledgments

- Django Documentation
- Stripe API Documentation
- Anthropic Claude for assistance
