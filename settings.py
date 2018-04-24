
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h8g39idb0b=i!qsj=u&lkc7)c)4s%^+i-b(^ownv1_05%l9v6o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DB_MYSQL_DATABASE = 'quanchengchuji'
DB_MYSQL_HOST = '192.168.33.10'
DB_MYSQL_PORT = '3306'
DB_MYSQL_USER = 'root'
DB_MYSQL_PASSWORD = 'root'

REDIS_HOST = '192.168.33.10'
REDIS_PORT = 6379
REDIS_DB = 5


BASE_UPLOAD_FILE_URL = '/upload/'
UPLOAD_FILE_LOCAL_STORAGE_DIR = '/var/tmp/boxing'

OSS_URL = 'url'
OSS_KEY = 'key'
OSS_SECRET = 'secret'
OSS_BUCKET = 'bucket'

OSS_CONFIG = {
    'url': OSS_URL,
    'app_key': OSS_KEY,
    'app_secret': OSS_SECRET,
    'bucket': OSS_BUCKET
}

setting_local_file = os.path.join(BASE_DIR, 'settings_local.py')
if os.path.exists(setting_local_file):
    execfile(setting_local_file)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'biz'
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

# ROOT_URLCONF = 'boxing_console.urls'

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

AUTH_USER_MODEL = 'biz.User'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_MYSQL_DATABASE,
        'HOST': DB_MYSQL_HOST,
        'PORT': DB_MYSQL_PORT,
        'USER': DB_MYSQL_USER,
        'PASSWORD': DB_MYSQL_PASSWORD,
        'OPTIONS': {
            'charset': 'utf8mb4'
        },
        'TEST': {
            'CHARSET': 'utf8mb4',
        }
    }
}

REDIS_CONFIG = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'db': REDIS_DB
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
