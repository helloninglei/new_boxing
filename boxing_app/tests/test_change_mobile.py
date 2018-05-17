from rest_framework import status
from . import APILoginTestCase
from biz import redis_const, redis_client
from biz.models import User


class ChangeMobileTestCase(APILoginTestCase):
    def setUp(self):
        self.client.credentials(**self.authorization_header)
        redis_client.redis_client.setex(redis_const.SEND_VERIFY_CODE.format(mobile='19990000000'), 300, 567986)

    def test_change_mobile(self):
        response = self.client.post(path="/mobile/change", data={
            "mobile": "19990000000", "verify_code": "567989"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "短信验证码错误！")

        response = self.client.post(path="/mobile/change", data={
            "mobile": self.user.mobile, "verify_code": "567989"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "手机号已绑定一个账号，不能再绑定！")

        response = self.client.post(path="/mobile/change", data={
            "mobile": "19990000000", "verify_code": "567986"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "ok")
        self.assertEqual(User.objects.get(id=self.user.id).mobile, "19990000000")
