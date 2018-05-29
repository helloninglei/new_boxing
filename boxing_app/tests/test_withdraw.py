from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User, WithdrawLog, UserProfile, MoneyChangeLog


class WithdrawTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(mobile="19999999908", password="password", money_balance=50000)
        UserProfile.objects.create(user=self.user)
        self.client = self.client_class()
        self.client.login(username=self.user.mobile, password="password")

    def test_withdraw(self):
        # 用户未绑定支付宝账号
        response = self.client.post(path="/withdraw", data={"amount": 30000}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "该用户未绑定支付宝账号，请先绑定支付宝账号！")

        UserProfile.objects.filter(user=self.user).update(alipay_account=self.user.mobile)

        # 未传amount
        response = self.client.post(path="/withdraw")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['amount'][0], "该字段是必填项。")

        # amount小于2元
        response = self.client.post(path="/withdraw", data={"amount": 100}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "提现金额必须大于2.0元!")

        # 账户余额不足提现金额
        response = self.client.post(path="/withdraw", data={"amount": 60000}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "提现金额不能大于账户余额!")

        # successfully
        response = self.client.post(path="/withdraw", data={"amount": 30000}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], "审核中")
        self.assertEqual(response.data['amount'], 30000)
        self.assertTrue(WithdrawLog.objects.filter(user=self.user).exists())
        self.assertTrue(MoneyChangeLog.objects.filter(user=self.user).exists())

        response = self.client.get(path="/withdraw")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
