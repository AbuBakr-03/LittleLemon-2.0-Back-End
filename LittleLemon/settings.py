# LittleLemon/settings.py
from pathlib import Path
import os
from datetime import timedelta
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", cast=str, default="")

DEBUG = config("DEBUG", cast=bool, default=False)

RAILWAY_ENVIRONMENT_NAME = os.getenv("RAILWAY_ENVIRONMENT_NAME")
if RAILWAY_ENVIRONMENT_NAME:
    DEBUG = False

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "*.railway.app",
    "*.up.railway.app",
    "api.littlelemon.restaurant",
]
# Filter out empty hosts
ALLOWED_HOSTS = [host for host in ALLOWED_HOSTS if host]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "LittleLemonApp",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "djoser",
    "django_filters",
    "storages",  # Add this for S3/R2 storage
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # For static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "LittleLemon.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "LittleLemon.wsgi.application"

# Add these at the top of your settings.py
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl

load_dotenv()

# Replace the DATABASES section of your settings.py with this
tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": tmpPostgres.path.replace("/", ""),
        "USER": tmpPostgres.username,
        "PASSWORD": tmpPostgres.password,
        "HOST": tmpPostgres.hostname,
        "PORT": 5432,
        "OPTIONS": dict(parse_qsl(tmpPostgres.query)),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

DJOSER = {"USER_ID_FIELD": "username", "DOMAIN": "littlelemon.restaurant"}

# Fixed JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=20),
    "ROTATE_REFRESH_TOKENS": False,  # CHANGED: Disable rotation for now
    "BLACKLIST_AFTER_ROTATION": False,  # CHANGED: Disable blacklisting
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}

# Cloudflare R2 Configuration
CLOUDFLARE_R2_BUCKET = config("CLOUDFLARE_R2_BUCKET", cast=str, default="")
CLOUDFLARE_R2_ACCESS_KEY = config("CLOUDFLARE_R2_ACCESS_KEY", cast=str, default="")
CLOUDFLARE_R2_SECRET_KEY = config("CLOUDFLARE_R2_SECRET_KEY", cast=str, default="")
CLOUDFLARE_R2_BUCKET_ENDPOINT = config(
    "CLOUDFLARE_R2_BUCKET_ENDPOINT", cast=str, default=""
)

if CLOUDFLARE_R2_BUCKET:
    CLOUDFLARE_R2_CONFIG_OPTIONS = {
        "bucket_name": CLOUDFLARE_R2_BUCKET,
        "access_key": CLOUDFLARE_R2_ACCESS_KEY,
        "secret_key": CLOUDFLARE_R2_SECRET_KEY,
        "endpoint_url": CLOUDFLARE_R2_BUCKET_ENDPOINT,
        "default_acl": "public-read",
        "signature_version": "s3v4",
    }

    STORAGES = {
        "default": {
            "BACKEND": "helpers.cloudflare.storages.MediaFileStorage",
            "OPTIONS": CLOUDFLARE_R2_CONFIG_OPTIONS,
        },
        "staticfiles": {
            "BACKEND": "helpers.cloudflare.storages.StaticFileStorage",
            "OPTIONS": CLOUDFLARE_R2_CONFIG_OPTIONS,
        },
    }


# Fixed CORS Settings
CORS_ALLOWED_ORIGINS = [
    "https://littlelemon.restaurant",
    "https://www.littlelemon.restaurant",
    "http://127.0.0.1:5175",  # Your actual frontend URL
    "http://localhost:5175",
]

CORS_ALLOW_CREDENTIALS = True

# Add these for file uploads
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "APIBackend": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
