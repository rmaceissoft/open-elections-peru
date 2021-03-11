"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROJECT_DIR = BASE_DIR / 'project'

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])

# Email backend to use
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")

# Host for sending email.
EMAIL_HOST = env("EMAIL_HOST", default="localhost")

# Port for sending email.
EMAIL_PORT = env("EMAIL_PORT", default=25)

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)

# Default email address
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="webmaster@localhost")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # third-party apps

    # project apps
    'app.shared',
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

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""

# Databases
# =====================================
# NOTE: DATABASE_URL format:
#       postgres://USER:PASSWORD@HOST:PORT/NAME
#       See: https://github.com/kennethreitz/dj-database-url

DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="postgres://postgres:postgres@db/postgres"
    )
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Default file storage mechanism that holds media.
DEFAULT_FILE_STORAGE = env(
    'DEFAULT_FILE_STORAGE', default='django.core.files.storage.FileSystemStorage')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = PROJECT_DIR / 'collected-static'

STATIC_URL = '/static/'

STATICFILES_DIRS = [PROJECT_DIR / "static"]

MEDIA_ROOT = PROJECT_DIR / 'media'

MEDIA_URL = '/media/'


# Cache
# =====================================

# The default number of seconds to cache a page for the cache middleware.
CACHE_MIDDLEWARE_SECONDS = env("CACHE_MIDDLEWARE_SECONDS", default=10 * 60)
CACHE_TIMEOUT = env("CACHE_TIMEOUT", default=60 * 60)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": CACHE_TIMEOUT,
    }
}

REDIS_URL = env("REDIS_URL", default="")

if REDIS_URL:
    CACHES["default"]["BACKEND"] = "redis_cache.RedisCache"
    CACHES["default"]["LOCATION"] = REDIS_URL


# Celery
# =====================================

CELERY_BROKER_URL = REDIS_URL

CELERY_RESULT_BACKEND = REDIS_URL


# TinyMCE config
# =====================================
TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 500,
    "menubar": False,
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
               "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
               "code,help,wordcount",
    "toolbar": "undo redo | formatselect | "
               "bold italic backcolor | alignleft aligncenter "
               "alignright alignjustify | bullist numlist outdent indent | "
               "image | code",
    "relative_urls": False
}


# VTiger
# =====================================

VTIGER_BASE_URL = env("VTIGER_BASE_URL", default="")
VTIGER_USERNAME = env("VTIGER_USERNAME", default="")
VTIGER_ACCESS_KEY = env("VTIGER_ACCESS_KEY", default="")


# Django-Import-Export-Celery
# =====================================

def policy_resource():
    from app.policies.admin import PolicyResource
    return PolicyResource


IMPORT_EXPORT_CELERY_MODELS = {
    "Policy": {
        "app_label": "app_policies",
        "model_name": "Policy",
        "resource": policy_resource
    }
}
IMPORT_EXPORT_CELERY_INIT_MODULE = 'app.celery'


# DropBox. Required by DropBoxStorage
# =====================================

DROPBOX_OAUTH2_TOKEN = env("DROPBOX_OAUTH2_TOKEN", default="")
DROPBOX_ROOT_PATH = env("DROPBOX_ROOT_PATH", default="/")
DROPBOX_TIMEOUT = env("DROPBOX_TIMEOUT", default=100)
DROPBOX_WRITE_MODE = env("DROPBOX_WRITE_MODE", default="add")


# FileBrowser Settings
# =====================================

FILEBROWSER_DEFAULT_PERMISSIONS = env("FILEBROWSER_DEFAULT_PERMISSIONS", default=None)
