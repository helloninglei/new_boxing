from rest_framework import status
from rest_framework.test import APITestCase
from biz.models import User, UserProfile
from biz import redis_const, redis_client


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        User.objects.create_user(mobile="19900000000", password="password")

    def test_mobile_register_status(self):
        response = self.client.get(path="/mobile_register_status", data={"mobile": "19900000000"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['result'])

        response = self.client.get(path="/mobile_register_status", data={"mobile": "19900000001"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['result'])

    def test_register(self):
        mobile = "18800000000"
        redis_client.redis_client.setex(redis_const.SEND_VERIFY_CODE.format(mobile=mobile), 300, "123456")

        response = self.client.post(path="/register",
                                    data={"mobile": mobile, "password": "password", "verify_code": "123456"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(redis_client.redis_client.exists(redis_const.REGISTER_INFO.format(mobile=mobile)))
        self.assertEqual(response.data['result'], "ok")
        response = self.client.post(path="/register_with_user_info", data={
            "mobile": mobile, "gender": True, "avatar": "avatar", "nick_name": "nick_name"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['result'], "ok")
        self.assertTrue(User.objects.filter(mobile=mobile))
        self.assertTrue(UserProfile.objects.filter(user__mobile=mobile).exists())
        self.assertFalse(redis_client.redis_client.exists(redis_const.REGISTER_INFO.format(mobile=mobile)))
