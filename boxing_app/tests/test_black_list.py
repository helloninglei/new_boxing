from rest_framework import status
from . import APILoginTestCase
from biz import redis_client
from biz.models import User


class BlackListTestCase(APILoginTestCase):
    def setUp(self):
        self.client.credentials(**self.authorization_header)
        self.user2 = User.objects.create_user(mobile="13300000000", password="password")

    def test_black_list(self):
        # 加入黑名单
        response = self.client.post(path=f"/black_list/{self.user2.id}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(redis_client.is_black_user(self.user.id, self.user2.id))

        # 在不在黑名单中
        response = self.client.get(path=f"/black_list/{self.user2.id}")
        self.assertTrue(response.data['result'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 获取黑名单列表
        response = self.client.get(path="/black_list")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertSetEqual(response.data['result'], {f"{self.user2.id}"})

        # 移出黑名单
        response = self.client.delete(path=f"/black_list/{self.user2.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(redis_client.is_black_user(self.user.id, self.user2.id))
