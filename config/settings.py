import os
from datetime import timedelta
from pathlib import Path
from decouple import config, Csv

# Directorio base
BASE_DIR = Path(__file__).resolve().parent.parent

# Carga de variables desde .env (para llaves que no rompen la app si faltan)
SECRET_KEY    = config('SECRET_KEY', default='test_secret_key_provisional_12345')
DEBUG         = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Terceros
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'corsheaders',
    
    # Apps Propias
    'dietetic',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

# CONFIGURACIÓN DE POSTGRESQL (Corregida sin 'config')
# REEMPLAZA 'TU_CONTRASEÑA_DE_PGADMIN' por tu clave real
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     'dietetic',
        'USER':     'postgres',
        'PASSWORD': 'postgres',  
        'HOST':     'localhost',
        'PORT':     '5432',
        'TEST': {
            'NAME': 'consulta_dietetica_test_db',
        },
    }
}

# Internacionalización
LANGUAGE_CODE = 'es-ec'
TIME_ZONE     = 'America/Guayaquil'
USE_I18N      = True
USE_TZ        = True

# Estáticos
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':     timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME':    timedelta(days=1),
    'ROTATE_REFRESH_TOKENS':     True,
    'BLACKLIST_AFTER_ROTATION':  True,
    'ALGORITHM':                 'HS256',
    'SIGNING_KEY':               SECRET_KEY,
    'AUTH_HEADER_TYPES':         ('Bearer',),
    'USER_ID_FIELD':             'id',
    'USER_ID_CLAIM':             'user_id',
}

# CORS
CORS_ALLOW_ALL_ORIGINS = True