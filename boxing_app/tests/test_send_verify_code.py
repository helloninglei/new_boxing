from rest_framework.test import APITestCase
from rest_framework import status
from biz import redis_client
from biz.redis_const import SENDING_VERIFY_CODE


class SendVerifyCodeVerify(APITestCase):
    def setUp(self):
        self.client = self.client_class()

    def test_send_verify_code(self):
        redis_client.redis_client.delete(SENDING_VERIFY_CODE.format(mobile="13300000000"))
        response = self.client.post(path='/verify_code', data={"mobile": "13300000000"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(path='/verify_code', data={"mobile": "13300000000"})
        self.assertEqual(response.data['message'][0], "需要图形验证码！")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        redis_client.redis_client.delete(SENDING_VERIFY_CODE.format(mobile="13300000000"))
        response = self.client.post(path="/verify_code", data={"mobile": "13300000000"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
