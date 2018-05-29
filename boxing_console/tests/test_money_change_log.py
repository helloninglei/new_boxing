from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User, MoneyChangeLog
from biz.constants import MONEY_CHANGE_TYPE_INCREASE_RECHARGE


class MoneyChangeLogTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(mobile="19990000000", password="password")
        self.client = self.client_class()
        self.client.login(username=self.user.mobile, password="password")

    def test_money_change_log_list(self):
        MoneyChangeLog.objects.create(user=self.user, change_type=MONEY_CHANGE_TYPE_INCREASE_RECHARGE,
                                      last_amount=0, change_amount=100000, remain_amount=100000, operator=self.user)
        MoneyChangeLog.objects.create(user=self.user, change_type=MONEY_CHANGE_TYPE_INCREASE_RECHARGE,
                                      last_amount=100000, change_amount=100000, remain_amount=200000, operator=self.user)

        response = self.client.get(path="/money_change_logs")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
