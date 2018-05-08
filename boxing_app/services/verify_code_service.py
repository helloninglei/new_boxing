import random


def send_verify_code(mobile):
    verify_code = random.randint(100000, 999999)
    return

    #
    # def send_verify_code(mobile, is_voice, ip):
    #     verify_code = random.randint(1000, 9999)
    #     verify_code_redis_key = redis_client.get_sms_verify_code_key(mobile)
    #     redis_client.setex(verify_code_redis_key, 60 * 10, verify_code)
    #     return sms_dayu.send_verify_code(str(mobile), str(verify_code), is_voice, ip)
