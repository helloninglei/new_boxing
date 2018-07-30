# coding: utf-8
import redis
from time import time
from datetime import datetime
from django.conf import settings
from django.db.models import F

from biz.models import UserProfile
from biz.redis_const import SHUTUP_LIST

PAGE_SIZE = settings.REST_FRAMEWORK['PAGE_SIZE']

redis_client = redis.StrictRedis(host=settings.REDIS_HOST,
                                 port=settings.REDIS_PORT,
                                 db=settings.REDIS_DB,
                                 max_connections=settings.REDIS_MAX_CONNECTIONS,
                                 decode_responses=True)


def _get_timestamp():
    return int(time())


def follow_user(current_user_id, follower_id):
    if not is_following(current_user_id, follower_id) and current_user_id != follower_id:
        p = redis_client.pipeline()
        p.zadd(f'follower_{follower_id}', _get_timestamp(), current_user_id)
        p.zadd(f'following_{current_user_id}', _get_timestamp(), follower_id)
        p.execute()
        UserProfile.objects.filter(user__id=follower_id).update(follower_count=F('follower_count') + 1)


def unfollow_user(current_user_id, follower_id):
    p = redis_client.pipeline()
    p.zrem(f'follower_{follower_id}', current_user_id)
    p.zrem(f'following_{current_user_id}', follower_id)
    p.execute()
    UserProfile.objects.filter(user__id=follower_id).update(follower_count=F('follower_count') - 1)


def is_follower(current_user_id, follower_id):
    return redis_client.zscore(f'follower_{current_user_id}', follower_id)


def is_following(current_user_id, follower_id):
    return redis_client.zscore(f'following_{current_user_id}', follower_id)


def follower_list(current_user_id, page=1):
    return redis_client.zrevrange(f'follower_{current_user_id}', PAGE_SIZE * (page - 1), PAGE_SIZE * page - 1)


def follower_list_all(current_user_id):
    return redis_client.zrevrange(f"follower_{current_user_id}", 0, -1)


def following_list(current_user_id, page=1):
    return redis_client.zrevrange(f'following_{current_user_id}', PAGE_SIZE * (page - 1), PAGE_SIZE * page - 1)


def following_list_all(current_user_id):
    return redis_client.zrevrange(f'following_{current_user_id}', 0, -1)


def follower_count(current_user_id):
    return redis_client.zcard(f'follower_{current_user_id}')


def following_count(current_user_id):
    return redis_client.zcard(f'following_{current_user_id}')


def record_object_location(obj, longitude, latitude):
    return redis_client.geoadd(f'{obj._meta.model_name}-location-set', longitude, latitude, obj.id)


def get_object_location(obj):
    return redis_client.geopos(f'{obj._meta.model_name}-location-set', obj.id)


def del_object_location(obj):
    return redis_client.zrem(f'{obj._meta.model_name}-location-set', obj.id)


def get_near_object(obj_or_cls, longitude, latitude, radius=10000, unit='km'):
    return redis_client.georadius(name=f'{obj_or_cls._meta.model_name}-location-set',
                                  longitude=longitude,
                                  latitude=latitude,
                                  radius=radius,
                                  unit=unit,
                                  withdist=True,
                                  sort='ASC')


# 加入黑名单
def block_user(current_user_id, black_user_id):
    if is_following(current_user_id, black_user_id):
        unfollow_user(current_user_id, black_user_id)
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


def get_order_no_serial():
    key = f'order_incr_{datetime.now().strftime("%Y%m%d")}'
    order_incr = redis_client.incr(key)
    if order_incr == 1:
        redis_client.expire(key, 3600 * 24)
    return str(order_incr).rjust(5, '0')


def forward_message(message_id):
    redis_client.hincrby('msg_forward', message_id, 1)


def get_message_forward_count(message_id):
    return int(redis_client.hget('msg_forward', message_id) or 0)


def set_user_title(user, title):
    return redis_client.set(f'user_{user.id}_title', title)


def get_user_title(user):
    return redis_client.get(f'user_{user.id}_title')


def del_user_title(user):
    return redis_client.delete(f'user_{user.id}_title')


# shut up list
def add_shutup_list(*user_ids):
    if user_ids:
        p = redis_client.pipeline()
        [p.zadd(SHUTUP_LIST, _get_timestamp(), user_id) for user_id in user_ids]
        p.execute()


def get_shutup_list():
    return redis_client.zrevrange(SHUTUP_LIST, 0, -1)


def rm_shutup_list(*user_ids):
    if user_ids:
        return redis_client.zrem(SHUTUP_LIST, *user_ids)
