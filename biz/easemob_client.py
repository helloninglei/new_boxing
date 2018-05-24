import requests
import json
from django.conf import settings
from biz import redis_const
from biz.redis_client import redis_client


class EaseMobClient:
    org_name = settings.EASEMOB_CONF['org_name']
    app_name = settings.EASEMOB_CONF['app_name']
    client_id = settings.EASEMOB_CONF['client_id']
    client_secret = settings.EASEMOB_CONF['client_secret']
    domain = settings.EASEMOB_CONF['url'] if settings.EASEMOB_CONF['url'].endswith("/") else \
        f"{settings.EASEMOB_CONF['url']}/"
    user_password = f"{org_name}pass"

    @classmethod
    def _get_token(cls):
        if redis_client.exists(redis_const.EASEMOB_TOKEN):
            return redis_client.get(redis_const.EASEMOB_TOKEN)
        resp = requests.post(url=f"{cls.domain}{cls.org_name}/{cls.app_name}/token", json={
            "grant_type": "client_credentials", "client_id": cls.client_id, "client_secret": cls.client_secret
        })
        resp_data = json.loads(resp.text)
        redis_client.setex(
            redis_const.EASEMOB_TOKEN, int(resp_data.get("expires_in")) - 60, resp_data.get("access_token"))
        return resp_data.get("access_token")

    @classmethod
    def batch_register(cls, *usernames):
        register_data = [{"username": username, "password": cls.user_password} for username in usernames]

        token = cls._get_token()
        resp = requests.post(
            url=f"{cls.domain}{cls.org_name}/{cls.app_name}/users",
            json=register_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        return resp
