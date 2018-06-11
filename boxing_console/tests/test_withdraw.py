from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User, UserProfile, WithdrawLog
from biz.constants import WITHDRAW_STATUS_WAITING, WITHDRAW_STATUS_APPROVED, WITHDRAW_STATUS_REJECTED


class WithdrawLogTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(mobile="19090909090", password="password")
        self.client = self.client_class()
        self.client.login(username=self.user.mobile, password="password")
        UserProfile.objects.filter(user=self.user).update(nick_name="nick_name")
        self.user.refresh_from_db()
        self.user2 = User.objects.create_user(mobile="19090909099", password="password")

    def test_withdraw_log_list(self):
        WithdrawLog.objects.create(user=self.user, amount=4000, status=WITHDRAW_STATUS_WAITING,
                                   withdraw_account=self.user.mobile, order_number="2018030200001",
                                   )
        WithdrawLog.objects.create(user=self.user2, amount=4000, status=WITHDRAW_STATUS_WAITING,
                                   withdraw_account=self.user2.mobile, order_number="2018030200002",
                                   )
        # search
        response = self.client.get(path="/withdraw_logs", data={"search": "2018030200002"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # filter
        response = self.client.get(path="/withdraw_logs", data={"status": "waiting"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_approved_withdraw(self):
        withdraw = WithdrawLog.objects.create(user=self.user, amount=4000, status=WITHDRAW_STATUS_WAITING,
                                              withdraw_account=self.user.mobile, order_number="2018030200001"
                                              )
        response = self.client.put(path=f"/withdraw_logs/{withdraw.id}/approved")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WithdrawLog.objects.get(id=withdraw.id).status, WITHDRAW_STATUS_APPROVED)
        self.assertEqual(User.objects.get(id=self.user.id).money_balance, 0)

        response = self.client.put(path=f"/withdraw_logs/{withdraw.id}/approved")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "该条记录已经审核过了，不能重复审核！")

    def test_rejected_withdraw(self):
        withdraw = WithdrawLog.objects.create(
            user=self.user, amount=4000, status=WITHDRAW_STATUS_WAITING,
            withdraw_account=self.user.mobile, order_number="2018030200001"
        )
        response = self.client.put(path=f"/withdraw_logs/{withdraw.id}/rejected")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WithdrawLog.objects.get(id=withdraw.id).status, WITHDRAW_STATUS_REJECTED)
        self.assertEqual(User.objects.get(id=self.user.id).money_balance, 4000)

        response = self.client.put(path=f"/withdraw_logs/{withdraw.id}/approved")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "该条记录已经审核过了，不能重复审核！")
