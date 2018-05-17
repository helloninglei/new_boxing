from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User
from biz import redis_const, redis_client


class ChangePasswordTestCase(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user = User.objects.create_user(mobile="12299999999", password="password")

    def test_change_password(self):
        token = self.client.post(path='/login', data={
            "username": self.user.mobile, "password": "password"
        }).data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # 原密码错误
        response = self.client.post(
            path="/password/change", data={"old_password": "password1", "new_password": "password2"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "原密码错误！")

        # change password successfully
        response = self.client.post(
            path="/password/change", data={"old_password": "password", "new_password": "password2"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "ok")

    def tearDown(self):
        redis_client.redis_client.delete(redis_const.HAS_LOGINED.format(mobile=self.user.mobile))
