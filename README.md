# 🍋 Little Lemon Restaurant - Backend API

Django REST API backend for Little Lemon restaurant management system with JWT authentication and comprehensive booking/menu management.

![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django) ![DRF](https://img.shields.io/badge/DRF-3.x-ff1709?logo=django) ![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?logo=mysql)

## ✨ Features

- 🔐 **JWT Authentication** - Secure token-based auth with refresh
- 📅 **Booking System** - CRUD operations with date filtering
- 🍽️ **Menu Management** - Categories, items, and image uploads
- 👥 **User Management** - Registration, roles (admin/user)
- 🔍 **Advanced Filtering** - Date, search, and ordering
- 📱 **CORS Support** - Ready for frontend integration

## 🛠️ Tech Stack

- **Django 5.x** + Django REST Framework
- **MySQL** - Database
- **JWT** - Authentication (Simple JWT)
- **Djoser** - User management
- **Django CORS** - Cross-origin requests
- **Django Filters** - Advanced filtering

## 🚀 Quick Start

```bash
# Clone & setup
git clone <repo-url>
cd littlelemon-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### Database Configuration
Update `LittleLemon/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'littlelemondb',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## 📁 Project Structure

```
LittleLemon/
├── LittleLemon/        # Project settings
│   ├── settings.py     # Django configuration
│   └── urls.py         # Main URL routing
├── LittleLemonApp/     # Main app
│   ├── models.py       # Database models
│   ├── serializers.py  # DRF serializers
│   ├── views.py        # API views
│   └── urls.py         # App URL routing
└── manage.py
```

## 🔗 API Endpoints

### Authentication
```
POST /auth/jwt/create/     # Login
POST /auth/jwt/refresh/    # Refresh token
POST /auth/users/          # Register
POST /auth/logout/         # Logout
```

### Bookings
```
GET    /api/booking/       # List bookings (?date=YYYY-MM-DD)
POST   /api/booking/       # Create booking
GET    /api/booking/{id}/  # Get booking
PUT    /api/booking/{id}/  # Update booking
DELETE /api/booking/{id}/  # Delete booking
```

### Menu Items
```
GET    /api/menu/          # List menu items
POST   /api/menu/          # Create item (with image upload)
GET    /api/menu/{id}/     # Get item
PUT    /api/menu/{id}/     # Update item
DELETE /api/menu/{id}/     # Delete item
```

### Categories
```
GET    /api/category/      # List categories
POST   /api/category/      # Create category
GET    /api/category/{id}/ # Get category
PUT    /api/category/{id}/ # Update category
DELETE /api/category/{id}/ # Delete category
```


```

## ⚙️ Configuration

### Key Settings
```python
# CORS for frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}
```

### Requirements.txt
```txt
Django>=5.0
djangorestframework
django-cors-headers
djangorestframework-simplejwt
djoser
django-filter
mysqlclient
Pillow  # For image uploads
```


## 🔧 Development Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Django shell
python manage.py shell
```


Built with Django + MySQL
