from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User, UserProfile
from biz import redis_const, redis_client


class BindAlipayAccountTestCase(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user = User.objects.create_user(mobile="16600000000", password='password')
        redis_client.redis_client.delete(redis_const.HAS_LOGINED.format(mobile=self.user.mobile))

    def test_bind_alipay_account(self):
        # 登录
        login_response = self.client.post(path='/login', data={
            "username": self.user.mobile, "password": "password"
        })

        # 获取短信验证码
        redis_client.redis_client.setex(redis_const.SEND_VERIFY_CODE.format(mobile=self.user.mobile), 300, "234567")

        # 数据不合法
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])

        response = self.client.post(path="/alipay_account", data={
            "alipay_account": "12200000000", "verify_code": "234568",
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "短信验证码错误！")

        # success
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        response = self.client.post(path="/alipay_account", data={
            "alipay_account": "12200000000", "verify_code": "234567",
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "ok")
        self.assertEqual(UserProfile.objects.get(user=self.user).alipay_account, "12200000000")
