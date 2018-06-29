from django.conf import settings
import django


def pytest_configure():
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
        'biz.hasher.BoxingMD5PasswordHasher',
    ]
    settings.REDIS_DB =15
    django.setup()
