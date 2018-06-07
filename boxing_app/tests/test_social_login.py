from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User


class SocialLoginTestCase(APITestCase):
    def setUp(self):
        self.client = self.client_class()

    def test_is_register(self):
        response = self.client.post(path="/social_login", data={"wechat_openid": "111", "weibo_openid": "222"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "wechat_openid、weibo_openid只能传一个！")

        response = self.client.post(path="/social_login", data={"wechat_openid": "111"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(bool(response.data['token']))

        User.objects.create_user(mobile="19999999999", password="password", wechat_openid=111)
        response = self.client.post(path="/social_login", data={"wechat_openid": "111"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(bool(response.data['token']))
