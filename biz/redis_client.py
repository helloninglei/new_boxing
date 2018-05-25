# coding: utf-8
import redis
from time import time
from django.conf import settings

PAGE_SIZE = settings.REST_FRAMEWORK['PAGE_SIZE']
_config = settings.REDIS_CONFIG
redis_client = redis.StrictRedis(host=_config['host'],
                                 port=_config['port'],
                                 db=_config['db'],
                                 max_connections=_config['max_connections'],
                                 decode_responses=True)


def _get_timestamp():
    return int(time())


def follow_user(current_user_id, follower_id):
    if not is_following(current_user_id, follower_id):
        p = redis_client.pipeline()
        p.zadd(f'follower_{follower_id}', _get_timestamp(), current_user_id)
        p.zadd(f'following_{current_user_id}', _get_timestamp(), follower_id)
        p.execute()


def unfollow_user(current_user_id, follower_id):
    p = redis_client.pipeline()
    p.zrem(f'follower_{follower_id}', current_user_id)
    p.zrem(f'following_{current_user_id}', follower_id)
    p.execute()


def is_follower(current_user_id, follower_id):
    return redis_client.zscore(f'follower_{current_user_id}', follower_id)


def is_following(current_user_id, follower_id):
    return redis_client.zscore(f'following_{current_user_id}', follower_id)


def follower_list(current_user_id, page=1):
    return redis_client.zrevrange(f'follower_{current_user_id}', PAGE_SIZE * (page - 1), PAGE_SIZE * page)


def following_list(current_user_id, page=1):
    return redis_client.zrevrange(f'following_{current_user_id}', PAGE_SIZE * (page - 1), PAGE_SIZE * page)


def following_list_all(current_user_id):
    return redis_client.zrevrange(f'following_{current_user_id}', 0, -1)


def follower_count(current_user_id):
    return redis_client.zcard(f'follower_{current_user_id}')


def following_count(current_user_id):
    return redis_client.zcard(f'following_{current_user_id}')


def record_boxing_club_location(club):
    return redis_client.geoadd('boxing-club-set', club.longitude, club.latitude, club.id)


def get_boxing_club_location(club_id):
    return redis_client.geopos('boxing-club-set', club_id)


def del_boxing_club_location(club_id):
    return redis_client.zrem('boxing-club-set', club_id)


# 加入黑名单
def block_user(current_user_id, black_user_id):
    return redis_client.sadd(f"user_{current_user_id}_black_list", black_user_id)


# 移出黑名单
def unblock_user(current_user_id, remove_user_id):
    return redis_client.srem(f"user_{current_user_id}_black_list", remove_user_id)


# 黑名单列表
def blocked_user_list(current_user_id):
    return redis_client.smembers(f"user_{current_user_id}_black_list")


# 是否在黑名单中
def is_blocked(current_user_id, user_id):
    return redis_client.sismember(f"user_{current_user_id}_black_list", user_id)


# 用户发布资源被分享次数
def incr_number_of_share(user_id):
    return redis_client.hincrby('sns_share', user_id, 1)


def get_number_of_share(user_id):
    return int(redis_client.hget('sns_share', user_id) or 0)
