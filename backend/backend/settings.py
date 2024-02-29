import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY', '')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # apps
    'user.apps.UserConfig',
    'payment.apps.PaymentConfig',

    # 3rd party apps
    'rest_framework',
    'djoser',
    'rest_framework.authtoken',
    'drf_spectacular',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'payments'),
        'USER': os.getenv('POSTGRES_USER', 'payments_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', 5432),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSESS': [
        'rest_framework.permissions.AllowAny'
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%S.%fZ",
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.yandex.ru')
EMAIL_PORT = os.getenv('EMAIL_PORT', 465)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'True')


CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379')
CELERY_RESULT_BACKEND = os.getenv(
    'CELERY_RESULT_BACKEND', 'db+sqlite:///celery.sqlite')


CACHES = {
    'default': {
        "BACKEND": 'django.core.cache.backends.redis.RedisCache',
        "LOCATION": os.getenv('REDIS_URL', 'redis://redis:6379'),
        'KEY_PREFIX': 'collect',
        'TIMEOUT': 60*15,
    }
}


DJOSER = {
    'LOGIN_FIELD': 'email'
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'Групповой сбор денег.',
    'DESCRIPTION': 'Тестовое задание Групповой сбор денег.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
