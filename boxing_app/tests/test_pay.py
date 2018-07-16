# -*- coding: utf-8 -*-
from datetime import datetime
from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase
from biz import constants
from biz.models import User, HotVideo, PayOrder
from biz.services.pay_service import PayService
from biz.constants import DEVICE_PLATFORM_IOS, PAYMENT_TYPE_ALIPAY, PAYMENT_STATUS_UNPAID, PAYMENT_STATUS_PAID
from django.contrib.contenttypes.fields import ContentType
from biz.redis_client import redis_client


class PaymentTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(mobile='11111111111', password='password')
        self.test_superuser = User.objects.create_superuser(mobile='11111111112', password='password')
        self.client1 = self.client_class(HTTP_SOURCE='iOS')
        self.client2 = self.client_class()
        self.client1.login(username=self.test_user, password='password')
        self.client2.login(username=self.test_superuser, password='password')

        self.data = {
            'name': 'test video1',
            'description': 'test video1',
            'price': 111,
            'url': '/videos/111',
            'try_url': '/videos/222',
            'operator_id': self.test_superuser.id,
        }

    @patch("biz.services.pay_service.PayService.generate_out_trade_no")
    def test_payment(self, generate_out_trade_no):
        generate_out_trade_no.return_value = f"{datetime.now().strftime('%m%d%H%M%S%f')}"
        video = HotVideo.objects.create(**self.data)
        video.users.add(self.test_user)
        payment_data = {
            'id': video.id,
            'payment_type': constants.PAYMENT_TYPE_WECHAT,
        }
        res = self.client1.post('/hot_videos/create_order', payment_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['pay_info'])
        self.assertTrue(res.data['order_id'])

        video_type = ContentType.objects.get_for_model(video)
        order = PayOrder.objects.get(content_type__pk=video_type.id, object_id=video.id)
        self.assertEqual(order.amount, self.data['price'])
        self.assertEqual(order.payment_type, constants.PAYMENT_TYPE_WECHAT)
        self.assertEqual(order.device, constants.DEVICE_PLATFORM_IOS)

        # test order no
        key = f'order_incr_{datetime.now().strftime("%Y%m%d")}'
        self.assertLessEqual(redis_client.ttl(key), 24 * 3600)

    def test_pay_status_info(self):
        video = HotVideo.objects.create(**self.data)
        video.users.add(self.test_user)

        order = PayService.perform_create_order(
            user=self.test_user,
            obj=video,
            device=DEVICE_PLATFORM_IOS,
            payment_type=PAYMENT_TYPE_ALIPAY,
        )

        res = self.client1.get('/pay_status', {'order_id': order.out_trade_no})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        PayOrder.objects.filter(out_trade_no=order.out_trade_no).update(status=PAYMENT_STATUS_PAID)
        res = self.client1.get('/pay_status', {'order_id': order.out_trade_no})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        result = res.data['result']
        self.assertEqual(result['status'], 'paid')
        self.assertEqual(result['amount'], self.data['price'])
        self.assertEqual(result['name'], f'视频（{self.data["name"]}）')

    def test_wallet_pay(self):
        video = HotVideo.objects.create(**self.data)
        video.users.add(self.test_user)
        payment_data = {
            'id': video.id,
            'payment_type': constants.PAYMENT_TYPE_WALLET,
        }
        res = self.client1.post('/hot_videos/create_order', payment_data)
        self.assertEqual(res.data['status'], 'failed')
        self.assertEqual(res.data['message'], '余额不足')

        self.test_user.money_balance = self.data['price'] * 100
        self.test_user.save()
        res = self.client1.post('/hot_videos/create_order', payment_data)
        order_id = res.data['order_id']
        self.assertEqual(res.data['status'], 'success')
        order = PayOrder.objects.get(out_trade_no=order_id)
        self.assertGreater(order.status, PAYMENT_STATUS_UNPAID)
