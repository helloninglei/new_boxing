from rest_framework.test import APITestCase
from rest_framework import status
from captcha.models import CaptchaStore
from rest_framework.authtoken.models import Token
from biz.redis_client import redis_client
from biz import redis_const
from biz.models import User


class LoginTestCase(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user1 = User.objects.create_user(mobile="17700000000", password="password")
        self.user2 = User.objects.create_superuser(mobile="17700000002", password="password")

    def test_login(self):
        self.client.get(path="/captcha-image")
        captcha = CaptchaStore.objects.all().order_by("-expiration").first()
        resp = self.client.post(path="/login", data={
            "username": self.user1.mobile, "password": "password", "captcha": {
                "captcha_code": captcha.response, "captcha_hash": captcha.hashkey
            }
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['message'][0], "该账号无登录权限!")

        self.client.get(path="/captcha-image")
        captcha = CaptchaStore.objects.all().order_by("-expiration").first()
        resp = self.client.post(path="/login", data={
            "username": self.user2.mobile, "password": "password", "captcha": {
                "captcha_code": captcha.response, "captcha_hash": captcha.hashkey
            }
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.get(user=self.user2).key, resp.data['token'])

    def tearDown(self):
        redis_client.delete(redis_const.HAS_LOGINED.format(mobile=self.user1.mobile))
        redis_client.delete(redis_const.HAS_LOGINED.format(mobile=self.user2.mobile))
