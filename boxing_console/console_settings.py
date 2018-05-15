"""
Django settings for boxing_console project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

from settings import *
from corsheaders.defaults import default_headers, default_methods

WSGI_APPLICATION = 'boxing_console.wsgi.application'

ROOT_URLCONF = 'boxing_console.urls'

REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ('rest_framework.permissions.IsAdminUser',)


PROJECT_PROPERTY = PROJECT_CONSOLE

AUTHENTICATION_BACKENDS = (
    'boxing_console.authentication_backends.StaffUserBackend',
)

INSTALLED_APPS += [
    'corsheaders',
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
] + MIDDLEWARE


CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = default_methods


CORS_ALLOW_HEADERS = default_headers
