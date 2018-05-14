"""
Django settings for boxing_app project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

from settings import *

ROOT_URLCONF = 'boxing_app.urls'

WSGI_APPLICATION = 'boxing_app.wsgi.application'

REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] = 'boxing_app.pagination.BoxingPagination'

PROJECT_PROPERTY = PROJECT_API
