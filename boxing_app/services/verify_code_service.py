from biz import redis_const, redis_client


def check_verify_code(mobile, verify_code):
    return verify_code == redis_client.redis_client.get(redis_const.SEND_VERIFY_CODE.format(mobile=mobile))
