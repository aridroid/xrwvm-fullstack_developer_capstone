"""
Django settings for djangoproj project.

Updated for local development so templates and static files load correctly.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-please-change-this-in-prod'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# For local development
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# If you publish to a real host / https domain later, add those hosts here:
# CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']
CSRF_TRUSTED_ORIGINS = []

# Django REST Framework (placeholder - add auth classes as needed)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
}

# Application definition
INSTALLED_APPS = [
    'djangoapp.apps.DjangoappConfig',   # your app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoproj.urls'

# Templates: include your djangoapp/templates folder so Home.html is found
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Keep both project-level templates and your app templates dir
        'DIRS': [
            BASE_DIR / 'djangoapp' / 'templates',   # your app templates (explicit)
            BASE_DIR / 'templates',                  # optional project-level templates
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',   # needed for `request` in templates
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoproj.wsgi.application'

# Database - default sqlite. Keep existing DB path if you have data.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Where your front-end static files live during development:
# Make sure this path exists or adjust it to where your static files are (e.g. frontend/static)
STATICFILES_DIRS = [
    BASE_DIR / 'frontend' / 'static',   # keep if you actually store static there
]

# If DEBUG=False or when deploying you will run collectstatic into STATIC_ROOT
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media (user uploaded files). Keep separate from static files.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
