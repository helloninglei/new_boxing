from rest_framework import status
from rest_framework.test import APITestCase
from biz.models import User, MoneyChangeLog
from biz import constants


class RechargeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(mobile=18900000000, password="password")
        self.client = self.client_class()
        self.client.login(username=self.user.mobile, password="password")

    def test_money_detail(self):
        money_change_log_income_data = dict(
            user=self.user, change_type=constants.MONEY_CHANGE_TYPE_INCREASE_RECHARGE,
            last_amount=0, change_amount=+20000, remain_amount=20000, operator=self.user
        )
        MoneyChangeLog.objects.create(**money_change_log_income_data)

        response = self.client.get(path="/recharge_log")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
