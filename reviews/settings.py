"""
Django settings for reviews project.
"""
import logging
import os
import configparser


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# config parser
# has precedence order -- later files override earlier ones
parser = configparser.ConfigParser()

# .env has environment and secrets
env_file = os.path.join(BASE_DIR, ".env")

try:
    parser.read(env_file)
except Exception:
    logging.critical("Unable to open .env file %s", env_file)
    raise

DEFAULT_CONFIG_SECTION = 'settings'
DATABASE_CONFIG_SECTION = 'database'

DJANGO_ENV = parser.get(DEFAULT_CONFIG_SECTION, 'DJANGO_ENV')

# <environment>.cfg holds environment-specific (non-secret) values
# it should be an ALL LOWERCASE file name that matches the environment name
CONFIG_DIR = 'config'
config_file = os.path.join(BASE_DIR, CONFIG_DIR, "%s.cfg" % DJANGO_ENV.lower())

try:
    parser.read(config_file)
except Exception:
    logging.critical("Unable to open config file %s", config_file)
    raise

# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SECRET_KEY = parser.get(DEFAULT_CONFIG_SECTION, 'SECRET_KEY')

DEBUG = parser.getboolean(DEFAULT_CONFIG_SECTION, 'DEBUG')

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework'
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

ROOT_URLCONF = 'reviews.urls'

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

WSGI_APPLICATION = 'reviews.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DB_ENGINE = parser.get(DATABASE_CONFIG_SECTION, 'DATABASE_ENGINE')
DB_NAME = parser.get(DATABASE_CONFIG_SECTION, 'DATABASE_NAME')
DB_USER = parser.get(DATABASE_CONFIG_SECTION, 'DATABASE_USER')
DB_PASSWORD = parser.get(DATABASE_CONFIG_SECTION, 'DATABASE_PASSWORD')
DB_HOST = parser.get(DATABASE_CONFIG_SECTION, 'DATABASE_HOST')
DB_PORT = parser.get(DATABASE_CONFIG_SECTION, 'DATABASE_PORT')

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
