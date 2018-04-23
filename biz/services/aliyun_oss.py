# coding: utf-8
import json
import time
import datetime
import base64
import hmac
from hashlib import sha1 as sha
from django.conf import settings

conf = settings.ALIYUN_OSS

def get_iso_8601(expire):
    gmt = datetime.datetime.fromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt

def get_token():
    now = int(time.time())
    expire_syncpoint  = now + conf.expire_time
    expire = get_iso_8601(expire_syncpoint)

    policy_dict = {}
    policy_dict['expiration'] = expire
    condition_array = []
    array_item = []
    array_item.append('starts-with')
    array_item.append('$key')
    array_item.append(conf.upload_dir)
    condition_array.append(array_item)
    policy_dict['conditions'] = condition_array 
    policy = json.dumps(policy_dict).strip()
    policy_encode = base64.b64encode(policy)
    h = hmac.new(conf.accessKeySecret, policy_encode, sha)
    sign_result = base64.encodestring(h.digest()).strip()

    token_dict = {
        'accessid': conf.accessKeyId,
        'host': conf.host,
        'policy': policy_encode,
        'signature': sign_result ,
        'expire': expire_syncpoint,
        'dir': conf.upload_dir
    }
    return token_dict