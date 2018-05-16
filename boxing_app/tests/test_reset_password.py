from rest_framework.test import APITestCase
from rest_framework import status
from captcha.models import CaptchaStore
from biz.models import User
from biz import redis_const, redis_client


class ResetPasswordTestCase(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user = User.objects.create_user(mobile="12299999999", password="password")

    def test_reset_password(self):
        # 请求参数错误
        response = self.client.post(path="/reset_password", data={
            "mobile": self.user.mobile, "password": "password1"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['verify_code'][0], "该字段是必填项。")
        self.assertEqual(response.data['captcha'][0], "该字段是必填项。")

        response = self.client.post(path="/reset_password", data={
            "mobile": self.user.mobile, "password": "password1", "verify_code": "234567",
            "captcha": {"captcha_code": "asked", "captcha_hash": "hi"}
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "图形验证码错误！")

        # reset password successfully
        redis_client.redis_client.setex(redis_const.SEND_VERIFY_CODE.format(mobile="12299999999"), 300, "234567")  # 短信验证码

        self.client.get(path="/captcha-image")
        captcha = CaptchaStore.objects.all().first()

        response = self.client.post(path="/reset_password", data={
            "mobile": self.user.mobile, "password": "password1", "verify_code": "234567",
            "captcha": {"captcha_code": captcha.response, "captcha_hash": captcha.hashkey}
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "ok")
        response = self.client.post(path="/login", data={
            "username": self.user.mobile, "password": "password1"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        redis_client.redis_client.delete(redis_const.HAS_LOGINED.format(mobile=self.user.mobile))
