import django
from django.conf import settings


def pytest_configure():
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
        'biz.hasher.BoxingMD5PasswordHasher',
    ]
    settings.REDIS_DB =15
    django.setup()
