import redis
from django.conf import settings

_config = settings.REDIS_CONFIG
redis_client = redis.StrictRedis(host=_config['host'],
                                 port=_config['port'],
                                 db=_config['db'],
                                 max_connections=_config['max_connections'])
