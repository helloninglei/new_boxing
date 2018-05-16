from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from biz.models import User
from biz.redis_client import redis_client
from biz import redis_const


class TestLogout(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user = User.objects.create_superuser(mobile="19900000000", password="password")
        redis_client.delete(redis_const.HAS_LOGINED.format(mobile=self.user.mobile))

    def test_logout(self):
        # 请求头未携带token
        response = self.client.delete(path="/logout")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "身份认证信息未提供。")

        # 请求头携带错误token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + "error_authorization")
        response = self.client.delete(path="/logout")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "认证令牌无效。")

        # token 正确
        self.client.credentials()
        response = self.client.post(path="/login", data={"username": self.user.mobile, "password": "password"})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])
        response = self.client.delete(path="/logout")
        self.assertEqual(response.data['message'], "ok")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def tearDown(self):
        redis_client.delete(redis_const.HAS_LOGINED.format(mobile=self.user.mobile))
