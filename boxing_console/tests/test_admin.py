from rest_framework import status
from biz.models import User
from rest_framework.test import APITestCase


class AdminTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(mobile="13330000000", password="password")
        self.super_user = User.objects.create_superuser(mobile="18880000000", password="password")
        self.client = self.client_class()
        self.client.login(username=self.super_user.mobile, password="password")

    def test_admin(self):

        # 列表
        resp = self.client.get(path="/admins")
        self.assertEqual(len(resp.data['results']), 1)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # 添加
        resp = self.client.post(path="/admins", data={"mobile": self.user.mobile})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.get(mobile=self.user.mobile).is_staff)

        resp = self.client.post(path="/admins", data={"mobile": self.user.mobile})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['message'][0], "该用户已是管理员，无需再添加！")

        resp = self.client.post(path="/admins", data={"mobile": "18976543212"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['message'][0], "该手机号未注册，请先在app注册！")

        # 删除
        resp = self.client.delete(path=f"/admins/{self.user.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.get(mobile=self.user.mobile).is_staff)
