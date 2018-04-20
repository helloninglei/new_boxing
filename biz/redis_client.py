# coding: utf-8

import redis
from django.conf import settings

_config = settings.REDIS_CONFIG
_client = redis.StrictRedis(host=_config['host'],
                            port=_config['port'],
                            db=_config['db'],
                            max_connections=200)


def exists(key):
    return _client.exists(key)


def set_incr(key, amount=1):
    return _client.incr(key, amount=amount)


def get_incr(key):
    return _client.incr(key)
