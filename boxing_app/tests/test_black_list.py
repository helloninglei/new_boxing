from rest_framework import status
from . import APILoginTestCase
from biz import redis_client
from biz.models import User
from biz.constants import SERVICE_USER_ID


class BlackListTestCase(APILoginTestCase):
    def setUp(self):
        self.client.credentials(**self.authorization_header)
        self.user2 = User.objects.create_user(mobile="13300000000", password="password")

    def test_black_list(self):
        # 加入黑名单
        response = self.client.post(path=f"/black_list/{self.user2.id}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(redis_client.is_blocked(self.user.id, self.user2.id))

        # 重复加入黑名单
        response = self.client.post(path=f"/black_list/{self.user2.id}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "不能重复添加黑名单！")

        # 加入黑名单的用户是官方账号
        response = self.client.post(path=f"/black_list/{SERVICE_USER_ID}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "官方账号不能加入黑名单!")

        # 在不在黑名单中
        response = self.client.get(path=f"/black_list/{self.user2.id}")
        self.assertTrue(response.data['result'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 获取黑名单列表
        response = self.client.get(path="/black_list")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data['result'], [{'id': self.user2.id, 'nick_name': None, 'avatar': None}])

        # 移出黑名单
        response = self.client.delete(path=f"/black_list/{self.user2.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(redis_client.is_blocked(self.user.id, self.user2.id))
