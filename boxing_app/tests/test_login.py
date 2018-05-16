from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from biz.models import User
from biz.redis_client import redis_client
from biz import redis_const


class TestLogin(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user = User.objects.create_user(mobile="19900000000", password="password")

    def test_login(self):
        response = self.client.post(path="/login", data={"username": self.user.mobile, "password": "password"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.get(key=response.data['token']).user.id, self.user.id)

    def tearDown(self):
        redis_client.delete(redis_const.HAS_LOGINED.format(mobile=self.user.mobile))
