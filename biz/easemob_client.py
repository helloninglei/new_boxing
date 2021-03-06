import requests
import json
from django.conf import settings
from biz import redis_const
from biz.redis_client import redis_client
from biz.constants import CHAT_ROOM_MAXUSERS


class EaseMobClient:
    org_name = settings.EASEMOB_CONF['org_name']
    app_name = settings.EASEMOB_CONF['app_name']
    client_id = settings.EASEMOB_CONF['client_id']
    client_secret = settings.EASEMOB_CONF['client_secret']
    domain = settings.EASEMOB_CONF['url'] if settings.EASEMOB_CONF['url'].endswith("/") else \
        f"{settings.EASEMOB_CONF['url']}/"
    user_password = "123456"
    get_users_limit = 1000
    chat_rooms_page_num = 1  # 环信获取聊天室，page num ，目前满足现有业务，业务不满足时，可更改
    chat_rooms_page_size = 10  # 环信获取聊天室，page size ，目前满足现有业务，业务不满足时，可更改

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

    @classmethod
    def send_text_messages(cls, msg, sender, *target):
        token = cls._get_token()
        url = f"{cls.domain}{cls.org_name}/{cls.app_name}/messages"
        json_data = {"target_type": "users", "target": target, "msg": {"type": "txt", "msg": msg},
                     "from": sender}
        return requests.post(url=url, json=json_data, headers={"Authorization": f"Bearer {token}"})

    @classmethod
    def get_users(cls):
        token = cls._get_token()
        url = f"{cls.domain}{cls.org_name}/{cls.app_name}/users?limit={cls.get_users_limit}"
        resp = requests.get(url=url, headers={"Authorization": f"Bearer {token}"})
        return [user['username'] for user in resp.json()['entities']]

    @classmethod
    def reset_user_password(cls):
        token = cls._get_token()
        usernames = cls.get_users()
        return [requests.put(url=f"{cls.domain}{cls.org_name}/{cls.app_name}/users/{username}/password",
                             json={"newpassword": cls.user_password}, headers={"Authorization": f"Bearer {token}"})
                for username in usernames]

    @classmethod
    def create_chatrooms(cls, name, description, owner, maxusers=CHAT_ROOM_MAXUSERS):
        token = cls._get_token()
        response = requests.post(url=f"{cls.domain}{cls.org_name}/{cls.app_name}/chatrooms",
                                 json={"name": name, "description": description, "owner": owner, "maxusers": maxusers,
                                       "members": []}, headers={"Authorization": f"Bearer {token}"})
        return response.json()

    @classmethod
    def get_chatrooms(cls):
        chat_rooms_info = redis_client.get(redis_const.EASEMOB_CHAT_ROOMS_INFO)
        if chat_rooms_info:
            return json.loads(chat_rooms_info)
        token = cls._get_token()
        response = requests.get(
            url=f"{cls.domain}{cls.org_name}/{cls.app_name}/chatrooms?pagenum={cls.chat_rooms_page_num}&pagesize={cls.chat_rooms_page_size}",
            headers={"Authorization": f"Bearer {token}"}
        )
        chat_rooms_info = response.json()['data']
        redis_client.set(redis_const.EASEMOB_CHAT_ROOMS_INFO, json.dumps(chat_rooms_info))
        return chat_rooms_info

    @classmethod
    def send_passthrough_message(cls, target: list, msg_type: str = "like"):
        token = cls._get_token()
        url = f"{cls.domain}{cls.org_name}/{cls.app_name}/messages"
        json_data = {
            "target_type": "users", "target": target, "msg": {"type": "cmd"}, "ext": {"msgType": msg_type}}
        return requests.post(url=url, json=json_data, headers={"Authorization": f"Bearer {token}"})
