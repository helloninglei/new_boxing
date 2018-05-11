# coding: utf-8
import redis
from time import time
from django.conf import settings

PAGE_SIZE = settings.REST_FRAMEWORK['PAGE_SIZE']
_config = settings.REDIS_CONFIG
_client = redis.StrictRedis(host=_config['host'],
                            port=_config['port'],
                            db=_config['db'],
                            max_connections=_config['max_connections'],
                            decode_responses=True)


def exists(key):
    return _client.exists(key)


def set_without_ex(key, value):
    return _client.set(key, value)


def setex(key, seconds, value):
    return _client.setex(key, seconds, value)


def incr(key):
    return _client.incr(key)


def get(key):
    return _client.get(key)


def delete(key):
    return _client.delete(key)


def hmset(key, mapping):
    return _client.hmset(key, mapping)


def hmget(key, fields):
    return _client.hmget(key, fields)


def _get_timestamp():
    return int(time())


def follow_user(current_user_id, follower_id):
    if not is_followed(current_user_id, follower_id):
        p = _client.pipeline()
        p.zadd(f'follower_{follower_id}', _get_timestamp(), current_user_id)
        p.zadd(f'followed_{current_user_id}', _get_timestamp(), follower_id)
        p.execute()


def unfollow_user(current_user_id, follower_id):
    p = _client.pipeline()
    p.zrem(f'follower_{follower_id}', current_user_id)
    p.zrem(f'followed_{current_user_id}', follower_id)
    p.execute()


def is_follower(current_user_id, follower_id):
    return _client.zscore(f'follower_{current_user_id}', follower_id)


def is_followed(current_user_id, follower_id):
    return _client.zscore(f'followed_{current_user_id}', follower_id)


def follower_list(current_user_id, page=1):
    return _client.zrevrange(f'follower_{current_user_id}', PAGE_SIZE * (page-1), PAGE_SIZE * page)


def followed_list(current_user_id, page=1):
    return _client.zrevrange(f'followed_{current_user_id}', PAGE_SIZE * (page-1), PAGE_SIZE * page)


def followed_list_all(current_user_id):
    return _client.zrevrange(f'followed_{current_user_id}', 0, -1)


def follower_count(current_user_id):
    return _client.zcard(f'follower_{current_user_id}')


def followed_count(current_user_id):
    return _client.zcard(f'followed_{current_user_id}')

def record_boxing_club_location(club):
    return _client.geoadd('boxing-club-set', club.longitude, club.latitude, club.pk)

def get_boxing_club_location(club_id):
    return _client.geopos('boxing-club-set', club_id)

def del_boxing_club_location(club_id):
    return _client.zrem('boxing-club-set',club_id)