"""
Django settings for magazine project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

import boto3
import redis
from corsheaders.defaults import default_headers, default_methods
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.getenv('DEBUG', default=0))

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', default='localhost').split(' ')

# CORS
# https://pypi.org/project/django-cors-headers/

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    *default_methods,
)

CORS_ALLOW_HEADERS = (
    *default_headers,
)

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_spectacular',
    'storages',
    'django_celery_beat',
    'corsheaders',
    'django_filters',
    'polymorphic',
    'debug_toolbar',
]

PROJECT_APPS = [
    'core',
    'users',
    'addresses',
    'fileflow',
    'outlets',
    'products',
    'attributes',
    'warehouses',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # debug_toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'magazine.urls'

TEMPLATES_DIR = Path(BASE_DIR).joinpath('templates').resolve()

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'magazine.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

# django-dbbackup
DBBACKUP_CONNECTORS = {
    'default': {
        'CONNECTOR': 'dbbackup.db.postgresql.PgDumpBinaryConnector',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
AWS_S3_USE_SSL = int(os.getenv('AWS_S3_USE_SSL', default=0))
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

STATIC_BUCKET_NAME = os.getenv('STATIC_BUCKET_NAME')
MEDIA_BUCKET_NAME = os.getenv('MEDIA_BUCKET_NAME')
DATABASE_BUCKET_NAME = os.getenv('DATABASE_BUCKET_NAME')

USE_S3 = int(os.getenv('USE_S3', default=0))

if USE_S3:
    STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/{STATIC_BUCKET_NAME}/'
    STATICFILES_STORAGE = 'magazine.storages.StaticStorage'

    MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{MEDIA_BUCKET_NAME}/'
    DEFAULT_FILE_STORAGE = 'magazine.storages.MediaStorage'

    DBBACKUP_STORAGE = 'magazine.storages.DataBaseStorage'
    DBBACKUP_STORAGE_OPTIONS = {
        'access_key': AWS_ACCESS_KEY_ID,
        'secret_key': AWS_SECRET_ACCESS_KEY,
        'bucket_name': DATABASE_BUCKET_NAME,
        'default_acl': 'private',
    }
else:
    STATIC_URL = '/static/'

    MEDIA_URL = '/media/'
    MEDIA_ROOT = Path(BASE_DIR).joinpath('media').resolve()

    DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
    DBBACKUP_STORAGE_OPTIONS = {
        'location': Path(BASE_DIR).joinpath('backup').resolve()
    }

STATICFILES_DIRS = (BASE_DIR / 'static',)
STATIC_ROOT = Path(BASE_DIR).joinpath('staticfiles').resolve()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

S3_CLIENT = boto3.client(
    's3',
    use_ssl=AWS_S3_USE_SSL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    endpoint_url=AWS_S3_ENDPOINT_URL
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REDIS
# https://redis.io/docs/
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

IS_TEST = int(os.getenv('IS_TEST', default=0))

if IS_TEST:
    REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
    REDIS_CLIENT_DATA = {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'db': 0,
    }
else:
    REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
    REDIS_CLIENT_DATA = {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'db': 0,
        'password': REDIS_PASSWORD
    }

REDIS_CLIENT = redis.StrictRedis(**REDIS_CLIENT_DATA)


# CELERY
# https://django.fun/ru/docs/celery/5.1/getting-started/introduction/

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL


# CELERY BEAT
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# CACHE BACKEND
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Celery debugger
if DEBUG:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_TASK_IGNORE_RESULT = True


# REST_FRAMEWORK
# https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# DJOSER
# https://djoser.readthedocs.io/en/latest/

DJOSER = {
    'REGISTER_URL': 'api/users/',
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'user': ('rest_framework.permissions.IsAuthenticated',),
        'user_list': ('rest_framework.permissions.IsAdminUser',),
    },
    'SERIALIZERS': {
        'user': 'users.serializers.UserSerializer',
        'user_list': 'users.serializers.UserSerializer',
        'current_user': 'users.serializers.UserSerializer',
        'user_create': 'users.serializers.UserSerializer',
    },
}