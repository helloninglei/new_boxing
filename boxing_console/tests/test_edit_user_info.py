from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User, MoneyChangeLog


class EditUserInfo(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user = User.objects.create_superuser(mobile="19999999990", password="password")
        self.user2 = User.objects.create_user(mobile="18888888881", password="password")
        self.client.login(username=self.user.mobile, password="password")

    def test_edit_user(self):
        update_data = {"title": "我是大名人", "user_type": "拳手", "change_amount": 10000}
        response = self.client.put(path=f"/edit_user/{self.user2.id}", data=update_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "不能编辑用户为拳手！")

        update_data['user_type'] = "名人"
        response = self.client.put(path=f"/edit_user/{self.user2.id}", data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], update_data['title'])
        self.assertEqual(response.data['user_type'], update_data['user_type'])
        self.assertEqual(response.data['money_balance'], self.user2.money_balance + update_data['change_amount'])

        self.user2.refresh_from_db()
        self.assertEqual(self.user2.money_balance, update_data['change_amount'])
        self.assertEqual(self.user2.title, update_data['title'])
        self.assertEqual(self.user2.get_user_type_display(), update_data['user_type'])

        self.assertTrue(MoneyChangeLog.objects.filter(user=self.user2, operator=self.user).exists())
