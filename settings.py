# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

import os
import raven
import sys
from base64 import b64decode
from corsheaders.defaults import default_headers, default_methods

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h8g39idb0b=i!qsj=u&lkc7)c)4s%^+i-b(^ownv1_05%l9v6o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

PRODUCTION = 'production'
TEST = 'test'
DEVELOPMENT = 'development'

ENVIRONMENT = DEVELOPMENT

ALLOWED_HOSTS = [
    '127.0.0.1',
    '39.105.73.10',  # qa1
    'localhost',
]

DB_MYSQL_DATABASE = 'quanchengchuji'
DB_MYSQL_HOST = '192.168.33.10'
DB_MYSQL_PORT = '3306'
DB_MYSQL_USER = 'root'
DB_MYSQL_PASSWORD = 'root'

DB_MYSQL_DATABASE_OLD = 'old_boxing'
DB_MYSQL_USER_OLD = DB_MYSQL_USER
DB_MYSQL_PASSWORD_OLD = DB_MYSQL_PASSWORD

# redis conf
REDIS_HOST = '192.168.33.10'
REDIS_PORT = 6379
REDIS_DB = 5
REDIS_MAX_CONNECTIONS = 200

# base url
BASE_URL = ""

SHARE_H5_BASE_URL = 'http://qa.bituquanguan.com/share/#/'

UPLOAD_URL_PATH = '/uploads/'

OSS_URL = 'url'
OSS_KEY = 'key'
OSS_SECRET = 'secret'
OSS_BUCKET = 'bucket'

OSS_CONFIG = {
    'url': OSS_URL,
    'app_key': OSS_KEY,
    'app_secret': OSS_SECRET,
    'bucket': OSS_BUCKET,
}

ALI_SMS_ACCESS_KEY_ID = 'key'
ALI_SMS_ACCESS_SECRET = 'secret'
ALI_SMS_INTERVAL = 60

app_private_key_string = """MIIEowIBAAKCAQEA0cU2PJy9CjkyFb2Mu9vcwF+79Fr++eL2FPGd2fpIpx3747GLE24iNnnGSgkcOtxyq+Kstpz90b2iF/Ni8q7zQW6tLND2LEh9Wx72lQwdkuiMKPB023qjcMvLeGoVxlkTrsS1M2xGnX+Mdo0CdzJcz2eCfrT8aTcGxFfhkZUCCVBZvP/7hXxjxP8jwrygf7dsCRuozLRlRib2EdaOdfMR1Uhnu8MZ4RScqCCZBk/e1wLE9E9Ooh5xHJU5enR8ZookQ+BlA2IONw8N7CsUcnQTdb7S748qeUjj3U+uLR/chEBNxMaZDwQKVuqW+Rt384GpQWPce/6S2PPsTjziu5Eh4QIDAQABAoIBAQCYMcqZDWtGiJrjFSSPhARU+uCGeKL4MIg0R90sMqAVx/ZijAUIsuZVueJ5AsUdm6YDObHvyFWLoFeDow2OYAqT1bYFhxKkrG9u9jcXirPGS7ytU1ClkQQWKXZVxjpIL4bNTWDej1donAsQVFyOmNankEUooy1jNQ5O1CgPlRnmILqFFhbmJSOUxnNIyf9GYaXW+tDA7CHW8uSliZMQHedNdqsEvaTkxy+992xOO0/zNld2JGGvaORnQxazFb7pMcRsztCiqgjakCfxUM/HirxUXEKko5Y+H6qo0qofISyjt8IjUboRPHP+qgFy9mdlc9RKL8NVUweRaEZI2mp4PBpxAoGBAPD50/wngApyO9goSsCOFbdXegvRhTBWUELOSfnBMq1BGt3ULGMMPTXH315vDFN4XQY+s9PrVgPtdGXetEPVXHwD6GkoPLSknTzzR9bghRPaxUElibhScJLu0TWg4jUDhG0wYUarV1qdrbamaFyVOHkzrwomnJmLTWDkufDYoXx1AoGBAN7ZUWp1GUR2CGMIZ4xO2spUFmnUeYGTl49QKDdL9YeokSN78GbH8OyZ2TBEMShH/ueIdsnzRKUyk6DMpo5LqxVECaKi80gzR0OzdTxZ9EaAFDsLQcodo5OQ1WfEakGFb/LYzfpPAh4B1aZWoXTcT7xmxxH/dtOLJYPlQHJDNVI9AoGAHCaTRRm4M4A0zYOnd+chUlG9yDOpw4PRzHwc2DhhmyvH37IxnUCIxgebaITAg9/Dvj8E8vTDD6JlvqDNnj8GltY+CErTDKdOVxh0g/2mjjM4Z+viss2uqPuNJR6uTlMi3T6RnpfVlJhm+rdl6ark9gO7pwvrr2Q+ndsafbBQ7SECgYAnemQ78caqJCbUNHbzmjyUP1VBJkzoMZdV4iNduG0kvS4JFTm/W4hIwfCB5nK26ho0Ni6lFB2DDnSstdSDvM/wEn+KekeS8NKdIbuRF3Z4ztPGqfXbsmh6CdxkZ51TQipU4SeMQlbjrfuFXi94HldZzvNRMuqAC1R4CzLhixp1GQKBgCYyxigrx6iBAUJqc/9IWxZCp79wn5BuKGDFX83Zv146P7B6lLfznJOqVE7IODTA8q8Umx/X00pzeYmi9UTNlseGfMEYjOwT2xBlbmMurBlSO7kJ6+A/BHFl4cdPdDcUQAmqPMPfwgA3suuaoeYZ8/y+mVnqigjnYb3gjwa5RSH2"""
alipay_public_key_string = """MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlr6mWRHPAsebrTocP50mX4F5IzrKrzRu1M9jBeEW7eFilDcIUEUbCUObAhvMMieELZTWSgp1HnOYyYzvX/GQE72xX+ka/EztnML4G4zUX8Y5uI2lTOki/daNLMOuxTAu0XSg9qEwyj6KTtu23gnZu9IlXqSs1rvCLtCBnbY37IGicjGhhflbrWb8ciE7AuS9eXAgs9K1Dw9EPdn3RuwcG8Ot0oEmjcxJl5hbtVzRNXJXgfRVrfoNNaEJwuvwXelE2LOj7VzNXkUPLXG/Y7v3AHsRDw/A5TfVGp+0boVDfLPt3l4Ghsci1nJx3UYLjKoZ2R2oWEn+Fkqww3NBxBiosQIDAQAB"""

# 沙箱环境

ALIPAY = {
    'appid': "2016082000301642",
    'app_notify_url': None,
    'app_private_key_string': b64decode(app_private_key_string),
    'alipay_public_key_string': b64decode(alipay_public_key_string),
    'sign_type': "RSA2",
    'debug': True
}

WECHAT_PAY = {
    'app_id': 'wxf0f79db974bc059f',
    'mch_id': '1482262802',
    'mch_key': 'Q7PQjXxqV6tawL6C0VvnPBktLCOt1ruO',
    'notify_url': 'http://118.187.56.164:60001/pay/wx/notify',
}

ANDROID_PACKAGE_NAME = 'com.douqu.boxing.test'
IOS_PACKAGE_NAME = 'com.douqu.boxing'
XIAOMI_PUSH_APP_SECRET_ANDROID = 'xiEtuYB4fZZzuort3lPD7A=='
XIAOMI_PUSH_APP_SECRET_IOS = 'RUtLcNFYgGdcy1eNIWZAcQ=='
# easemob conf
EASEMOB_CONF = {
    'app_name': 'boxing',
    'client_id': 'id',
    'client_secret': 'secret',
    'org_name': 'dou',
    'url': 'https://a1.easemob.com/'
}

# celery conf
BROKER_REDIS_DB = "0"

# baidu map api
BAIDU_MAP_URL = 'http://api.map.baidu.com/geocoder/v2/'
BAIDU_MAP_AK = 'KCzp8claYra8uYAvahElV9oKUT6j7Gx1'

# version conf
ANDROID_VERSION = {
    'version': '3.3.0',
    'version_code': '44',
    'url': '',
    'message': '3.3.0',
    'force': True
}

IOS_VERSION = {
    'version': '3.3.0',
    'message': '3.3.0',
    'force': True
}

OSS_BASE_URL = 'http://39.105.73.10'

WEIXIN_PUBLIC_PLATFORM_CONF = {
    "app_id": "",
    "app_secret": ""
}

SENTRY_DSN = 'http://ded6e41633544be1bd6e1f03454fe5c7:48dc8740b5ec42d58f9618649ffae5ec@39.104.180.65//2'
CDN_BASE_URL = ''

setting_local_file = os.path.join(BASE_DIR, 'settings_local.py')
if os.path.exists(setting_local_file):
    from settings_local import *

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "rest_framework.authtoken",
    'biz',
    'boxing_app',
    'boxing_console',
    'captcha',
    'django_filters',
    'corsheaders',
    'raven.contrib.django.raven_compat',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_MYSQL_DATABASE,
        'HOST': DB_MYSQL_HOST,
        'PORT': DB_MYSQL_PORT,
        'USER': DB_MYSQL_USER,
        'PASSWORD': DB_MYSQL_PASSWORD,
        'CONN_MAX_AGE': 120,
        'OPTIONS': {
            'charset': 'utf8mb4'
        },
        'TEST': {
            'CHARSET': 'utf8mb4',
        }
    },
    'old_boxing': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_MYSQL_DATABASE_OLD,
        'HOST': DB_MYSQL_HOST,
        'PORT': DB_MYSQL_PORT,
        'USER': DB_MYSQL_USER_OLD,
        'PASSWORD': DB_MYSQL_PASSWORD_OLD,
        'OPTIONS': {
            'charset': 'utf8mb4'
        },
        'TEST': {
            'CHARSET': 'utf8mb4',
        }
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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "biz.authentications.CsrfExemptSessionAuthentication",
    ),
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    "NON_FIELD_ERRORS_KEY": "message",
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# captcha conf
CAPTCHA_IMAGE_SIZE = (144, 66)
CAPTCHA_FONT_SIZE = 30
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_arcs',)

# project property
PROJECT_API = 'api'
PROJECT_CONSOLE = 'console'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = default_methods
CORS_ALLOW_HEADERS = default_headers

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'biz.hasher.BoxingMD5PasswordHasher',
]

RAVEN_CONFIG = {
    'dsn': SENTRY_DSN,
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(BASE_DIR),
}
