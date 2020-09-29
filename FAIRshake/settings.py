"""
Django settings for FAIRshake project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import re
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_URL = ''

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY_FILE = os.environ.get(
    'SECRET_KEY_FILE',
    '/ssl/secret.txt' if os.path.isfile('/ssl/secret.txt') else None
)

SECRET_KEY = '^r26!v-me2p&1(qaqr1m@h1n*@$t-57f!4sd9f$d3)xnk&kj9)' if SECRET_KEY_FILE is None else open(SECRET_KEY_FILE, 'r').read()

DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = [
    'localhost',
    'fairshake.cloud',
    'www.fairshake.cloud',
]

INTERNAL_IPS = (
    '127.0.0.1',
)

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'des',
    'drf_yasg',
    'rest_auth',
    'rest_auth.registration',
    'bootstrapform',
    'corsheaders',
    'ajax_select',
    'analytical',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.orcid',
    'allauth.socialaccount.providers.globus',
    'extensions.ajax_select_ex',
    'extensions.allauth_ex',
    'extensions.drf_yasg_ex',
    'extensions.rest_auth_ex',
    'extensions.rest_framework_ex',
    'FAIRshakeHub',
    'FAIRshakeAPI',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS += [
        'livereload',
        'debug_toolbar',
    ]
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'livereload.middleware.LiveReloadScript',
    ]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # TODO: fix pagination handling so these values can be different
    'PAGE_SIZE': 11,
    'VIEW_PAGE_SIZE': 11,
    'SEARCH_PAGE_SIZE': 11,
    'ASSESSMENTS_PAGE_SIZE': 25,
    'EXCEPTION_HANDLER': 'extensions.rest_framework_ex.exeptions.handler',
    'URL_FIELD_NAME': 'get_url',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': {
        'mozilla_django_oidc': {
            'handlers': ['console' if DEBUG else 'mail_admins'],
            'level': 'INFO' if DEBUG else os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
        'django': {
            'handlers': ['console' if DEBUG else 'mail_admins'],
            'level': 'INFO' if DEBUG else os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}

IGNORABLE_404_URLS = [
  re.compile(r'^/apple-touch-icon.*\.png$'),
  re.compile(r'^/favicon\.ico$'),
  re.compile(r'^/robots\.txt$'),
  re.compile(r'\.(php|cgi)$'),
  re.compile(r'^/phpmyadmin/'),
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
        }
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'FAIRshakeHub', 'templates',),
            os.path.join(BASE_DIR, 'extensions', 'allauth_ex', 'templates',),
            os.path.join(BASE_DIR, 'extensions', 'ajax_select_ex', 'templates',),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django.contrib.staticfiles.templatetags.staticfiles',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ROOT_URLCONF = 'FAIRshake.urls'

WSGI_APPLICATION = 'FAIRshake.wsgi.application'

AUTH_USER_MODEL = 'FAIRshakeAPI.Author'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

MYSQL_CONFIG = os.environ.get(
    'MYSQL_CONFIG',
    '/ssl/my.cnf' if os.path.isfile('/ssl/my.cnf') else None
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    } if MYSQL_CONFIG is None else {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': MYSQL_CONFIG,
            'init_command': 'SET max_execution_time=30000',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/' + BASE_URL + 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
        ],
    },
    'globus': {
        'SCOPE': [
            'openid',
            'profile',
            'email',
        ],
    },
}

LOGIN_URL = '/' + BASE_URL + 'accounts/login/'
LOGOUT_URL = '/' + BASE_URL + 'accounts/logout/'

LOGIN_REDIRECT_URL = '/' + BASE_URL
LOGOUT_REDIRECT_URL = '/' + BASE_URL

ACCOUNT_LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URL
ACCOUNT_LOGOUT_REDIRECT_URL = LOGOUT_REDIRECT_URL

LOGOUT_ON_PASSWORD_CHANGE = False

CORS_ORIGIN_ALLOW_ALL = True

SWAGGER_SETTINGS = {
    'DEFAULT_GENERATOR_CLASS': 'extensions.drf_yasg_ex.schema.CustomSchemaGenerator',
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic',
        },
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'schema': 'token',
        },
    },
}

GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-6277639-33'
GOOGLE_ANALYTICS_DISPLAY_ADVERTISING = False
GOOGLE_ANALYTICS_SITE_SPEED = True

EMAIL_BACKEND = 'des.backends.ConfiguredEmailBackend'

SERVER_EMAIL = 'danieljbclarkemssm@gmail.com'
ADMINS = [
  ('Daniel', 'danieljbclarkemssm@gmail.com',),
]

ASSESSMENT_CONFIG_FILE = os.environ.get(
    'ASSESSMENT_CONFIG_FILE',
    '/ssl/config.json' if os.path.isfile('/ssl/config.json') else None
)

ASSESSMENT_CONFIG = json.load(
    open(ASSESSMENT_CONFIG_FILE, 'r')
 ) if ASSESSMENT_CONFIG_FILE is not None else {}
