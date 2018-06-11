"""
Django settings for boxing_console project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

from settings import *

WSGI_APPLICATION = 'boxing_console.wsgi.application'

ROOT_URLCONF = 'boxing_console.urls'

REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ('rest_framework.permissions.IsAdminUser',)

PROJECT_PROPERTY = PROJECT_CONSOLE

AUTHENTICATION_BACKENDS = (
    'biz.authentication_backends.StaffUserBackend',
)
