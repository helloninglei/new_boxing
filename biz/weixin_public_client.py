import hashlib
import random
import string

import requests
import logging

import time
from django.conf import settings
from requests.exceptions import RequestException
from biz.redis_client import redis_client
from biz.redis_const import WEIXIN_PUBLIC_ACCESS_TOKEN, WEIXIN_PUBLIC_JSAPI_TICKET_KEY
from weixin.mp import WeixinMP

logger = logging.getLogger()


class WeiXinPublicPlatformClient:
    app_id = settings.WEIXIN_PUBLIC_PLATFORM_CONF['app_id']
    app_secret = settings.WEIXIN_PUBLIC_PLATFORM_CONF['app_secret']
    token_url = \
        f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    jsapi_ticket_url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={token}&type=jsapi"

    @classmethod
    def fetch_token(cls):
        token = redis_client.get(WEIXIN_PUBLIC_ACCESS_TOKEN)
        if token:
            return token
        try:
            response = requests.get(cls.token_url)
        except RequestException as e:
            logger.error(f'fetch weixin public access token error: {e}')
        else:
            result = response.json()
            if result.get("errcode"):
                logger.error(f"fetch weixin public access token failed, response: {result}")
            token = result.get("access_token")
            expires_in = result.get("expires_in")
            # redis_client.setex(WEIXIN_PUBLIC_ACCESS_TOKEN, int(expires_in) - 60, token)
            return token

    @classmethod
    def fetch_jsapi_ticket(cls):
        ticket = redis_client.get(WEIXIN_PUBLIC_JSAPI_TICKET_KEY)
        if ticket:
            return ticket
        token = cls.fetch_token()
        try:
            response = requests.get(cls.jsapi_ticket_url.format(token=token))
        except RequestException as e:
            logger.error(f"fetch weixin public jsapi ticket error: {e}")
        else:
            result = response.json()
            ticket = result.get("ticket")
            expires_in = result.get("expires_in")
            # redis_client.setex(WEIXIN_PUBLIC_JSAPI_TICKET_KEY, int(expires_in) - 60, ticket)
            return ticket


class Sign:
    """微信二次分享获取签名"""
    def __init__(self, url):
        self.ret = {
            'nonceStr': self._create_nonce_str(),
            'jsapi_ticket': WeiXinPublicPlatformClient.fetch_jsapi_ticket(),
            'timestamp': self._create_timestamp(),
            'url': url
        }

    def _create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def _create_timestamp(self):
        return int(time.time())

    def sign(self):
        string_ = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(string_.encode()).hexdigest()
        self.ret['app_id'] = settings.WEIXIN_PUBLIC_PLATFORM_CONF['app_id']
        self.ret['debug'] = settings.DEBUG
        return self.ret
