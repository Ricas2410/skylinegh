import os
import dj_database_url
from .settings import *

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, try to load manually
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ.setdefault(key, value)

# Production settings
DEBUG = False
# Allow hosts; default to '*' so internal IP health checks pass. Override via env if needed.
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# Database configuration using environment variable
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,  # 10 minutes connection pooling
            conn_health_checks=True,
        )
    }
else:
    # Fallback to individual environment variables
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
            'NAME': os.getenv('DB_NAME', 'skylinegh'),
            'USER': os.getenv('DB_USER', ''),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'OPTIONS': {
                'connect_timeout': 10,
            },
            'CONN_MAX_AGE': 600,
            'CONN_HEALTH_CHECKS': True,
        }
    }

# Database connection optimizations for cost savings
DATABASES['default'].update({
    'OPTIONS': {
        'connect_timeout': 10,
    },
    'CONN_MAX_AGE': 600,  # 10 minutes connection pooling
    'CONN_HEALTH_CHECKS': True,
})

# ImageKit configuration (must be provided via environment variables)
# Set these as secrets in Fly and locally for testing:
#   IMAGEKIT_PRIVATE_KEY, IMAGEKIT_PUBLIC_KEY, IMAGEKIT_URL_ENDPOINT
IMAGEKIT_PRIVATE_KEY = os.environ['IMAGEKIT_PRIVATE_KEY']
IMAGEKIT_PUBLIC_KEY = os.environ['IMAGEKIT_PUBLIC_KEY']
IMAGEKIT_URL_ENDPOINT = os.environ['IMAGEKIT_URL_ENDPOINT']

# Use ImageKit for media storage (Django 5+ via STORAGES)
STORAGES = {
    'default': {
        'BACKEND': 'core.storage.ImageKitStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}
MEDIA_URL = IMAGEKIT_URL_ENDPOINT + '/'

# Static files with WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
# Keep for backward compatibility (Django <5); STORAGES['staticfiles'] is authoritative in Django 5+
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = '/app/staticfiles'
STATICFILES_DIRS = [
    '/app/static',
]

# WhiteNoise configuration for optimal performance
WHITENOISE_USE_FINDERS = False  # Disable in production for performance
WHITENOISE_AUTOREFRESH = False  # Disable in production
WHITENOISE_MAX_AGE = 31536000  # 1 year cache for static files
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'zip', 'gz', 'tgz', 'bz2', 'tbz', 'xz', 'br']

# Security settings
# Disable SSL redirect so Fly's HTTP health checks to /healthz don't get 301s.
# Public traffic is still terminated at HTTPS by Fly's edge.
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Session and CSRF cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Optimized caching for better performance and cost savings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
        'TIMEOUT': 300,  # 5 minutes default
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 3,
        }
    }
}

# Cache sessions in database for better performance
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 86400  # 24 hours

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Performance optimizations for startup cost savings
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Template caching for better performance
TEMPLATES[0]['APP_DIRS'] = False  # Must be False when using custom loaders
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# Optimize middleware for performance
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',  # Cache middleware first
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',  # Cache middleware last
]

# Email backend for production (using console for now to save costs)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Optimize admin for production
ADMIN_URL = os.getenv('ADMIN_URL', 'admin/')  # Allow custom admin URL for security

# Compress responses to save bandwidth
USE_GZIP = True
