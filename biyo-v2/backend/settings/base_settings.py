# -*- coding: utf-8 -*-
"""
Django settings for pulsewallet project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys
import os
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# sys.path.insert(0, os.path.abspath(BASE_DIR))
# sys.path.insert(0, os.path.abspath((os.path.join(BASE_DIR, 'backend')))

AUTH_USER_MODEL = 'employees.Employee'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3ke-9huyhep%v&t6g9jju5%%hf@*&k$xc*+)z^_x=(-#14$a-w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

NEW_TEMP = True
#NEW_TEMP = False

ALLOWED_HOSTS = ['*']

MEDIA_ROOT = os.path.join(BASE_DIR, os.path.pardir, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, os.path.pardir, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STORAGE_ROOT = os.path.join(BASE_DIR, os.path.pardir, 'storage')
STORAGE_URL = '/storage/'

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, "fixtures"),
]


# Application definition

INSTALLED_APPS = (
    'suit',  # django-suit
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'corsheaders',
    'simple_history',
    'localflavor',
    'displays',
    'products',
    'payments',
    'panel',
    'order',
    'reports',
    # 'theme',
    # 'gunicorn',
    # 'mobileapi',
    'employees',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'terminalapi',
    # 'debug_toolbar',
    'rest_framework_swagger',
    'django_jenkins',
    'django_extensions',
    'django_countries',
    'django_filters',
    'betterforms',
    'taskin',
    'dbsettings',
    'purchase',
    'sorl.thumbnail',
    'bootstrap3',
    'mobile_api'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

AUTHENTICATION_BACKENDS = ('employees.backend.OwnerAuthModelBackend', )

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


if NEW_TEMP == True:
    TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templatesv2'), )
else:
    TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
    ('es', _('Spanish')),
    ('tr', _('Turkish')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, os.path.pardir, 'locale')
]
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_COOKIE_AGE = 60 * 20
SESSION_SAVE_EVERY_REQUEST = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

LOGIN_REDIRECT_URL = 'dashboard'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    # ),
    # 'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
}

SWAGGER_SETTINGS = {
    "exclude_namespaces": [],  # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '',  # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'suport'
EMAIL_HOST_PASSWORD = 'suportsuport'
EMAIL_PORT = 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = 'no-reply@dashboard.center'
ANONYMOUS_USER_ID = -1

CORS_ORIGIN_ALLOW_ALL = True
