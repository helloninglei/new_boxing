from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User


class TestLoginIsNeedCaptcha(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user = User.objects.create_user(mobile="19900000000", password="password")

    def test_login_is_need_captcha(self):
        self.client.post(path="/login", data={"username": self.user.mobile, "password": "password"})
        response = self.client.get(path="/login_is_need_captcha", data={"mobile": self.user.mobile})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['result'])

        # 手机号不合法
        response = self.client.get(path="/login_is_need_captcha", data={"mobile": "199000000"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['mobile'][0], "199000000 不是有效手机号。")

        # 手机号未输入
        response = self.client.get(path="/login_is_need_captcha", data={"mobile": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['mobile'][0], "该字段不能为空。")
