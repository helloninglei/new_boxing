from rest_framework import status
from rest_framework.test import APITestCase
from biz.models import User, PayOrder
from biz import constants
from biz.services.pay_service import PayService


class RechargeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(mobile=18900000000, password="password")
        self.client = self.client_class()
        self.client.login(username=self.user.mobile, password="password")

    def test_money_detail(self):
        pay_order_data = dict(
            user=self.user,
            status=constants.PAYMENT_STATUS_WAIT_USE,
            content_object=self.user,
            amount=1000,
            out_trade_no=PayService.generate_out_trade_no(),
            payment_type=constants.PAYMENT_TYPE_ALIPAY,
            device=constants.DEVICE_PLATFORM_IOS,
        )

        PayOrder.objects.create(**pay_order_data)

        response = self.client.get(path="/recharge_log")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
