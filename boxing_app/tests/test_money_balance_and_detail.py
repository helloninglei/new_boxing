from rest_framework import status
from rest_framework.test import APITestCase
from biz.models import User, MoneyChangeLog
from biz import constants


class MoneyBalanceTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(mobile=18900000000, password="password")
        self.client = self.client_class()
        self.client.login(username=self.user.mobile, password="password")

    def test_money_balance(self):
        response = self.client.get(path="/money_balance")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 0)

    def test_money_detail(self):
        money_change_log_income_data = dict(
            user=self.user, change_type=constants.MONEY_CHANGE_TYPE_INCREASE_RECHARGE,
            last_amount=0, change_amount=+20000, remain_amount=20000, operator=self.user
        )
        MoneyChangeLog.objects.create(**money_change_log_income_data)
        money_change_log_expend_data = dict(
            user=self.user, change_type=constants.MONEY_CHANGE_TYPE_REDUCE_ORDER,
            last_amount=20000, change_amount=-10000, remain_amount=10000, operator=self.user
        )
        MoneyChangeLog.objects.create(**money_change_log_expend_data)
        response = self.client.get(path="/money_change_log")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        # 收入
        response = self.client.get(path="/money_change_log", data={"keyword": "income"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['change_amount'],
                         f"+{money_change_log_income_data['change_amount']/100:.2f}")
        self.assertEqual(response.data['results'][0]['change_type'], "充值")

        # 支出
        response = self.client.get(path="/money_change_log", data={"keyword": "expend"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['change_amount'],
                         f"{money_change_log_expend_data['change_amount']/100:.2f}")
        self.assertEqual(response.data['results'][0]['change_type'], "约单(支出)")
