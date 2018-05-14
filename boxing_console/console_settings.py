"""
Django settings for boxing_console project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from settings import *
from corsheaders.defaults import default_headers, default_methods

WSGI_APPLICATION = 'boxing_console.wsgi.application'

ROOT_URLCONF = 'boxing_console.urls'

REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ('rest_framework.permissions.IsAdminUser',)


INSTALLED_APPS += [
    'corsheaders',
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
] + MIDDLEWARE


CORS_ORIGIN_WHITELIST = (
    '*',
)

CORS_ALLOW_METHODS = default_methods


CORS_ALLOW_HEADERS = default_headers
