# -*- coding: utf-8 -*-
import datetime
from biz import constants
from rest_framework.test import APITestCase
from biz.models import User, HotVideo, PayOrder
from biz.services.pay_service import PayService


class HotVideoTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(mobile='11111111111', password='password')
        self.test_superuser = User.objects.create_superuser(mobile='11111111112', password='password')
        self.test_user3 = User.objects.create_user(mobile='11111111113', password='password')
        self.client1 = self.client_class()
        self.client2 = self.client_class()
        self.client3 = self.client_class()
        self.client1.login(username=self.test_user, password='password')
        self.client2.login(username=self.test_superuser, password='password')
        self.client3.login(username=self.test_user3, password='password')

        self.data = {
            'user_id': self.test_user.id,
            'name': 'test video1',
            'description': 'test video1',
            'price': 111,
            'url': '/videos/111',
            'try_url': '/videos/222',
            'operator_id': self.test_superuser.id,
        }

    def test_video_payment(self):
        video = HotVideo.objects.create(**self.data)

        PayOrder.objects.create(
            user=self.test_user,
            status=constants.PAYMENT_STATUS_UNPAID,
            content_object=video,
            amount=video.price,
            out_trade_no=PayService.generate_out_trade_no(),
            payment_type=constants.PAYMENT_TYPE_ALIPAY,
            device=constants.DEVICE_PLATFORM_IOS,
        )
        PayOrder.objects.create(
            user=self.test_user3,
            status=constants.PAYMENT_STATUS_WAIT_USE,
            content_object=video,
            amount=video.price,
            out_trade_no=PayService.generate_out_trade_no(),
            payment_type=constants.PAYMENT_TYPE_ALIPAY,
            device=constants.DEVICE_PLATFORM_IOS,
            pay_time=datetime.datetime.now(),
        )

        res = self.client1.get(f'/users/{self.test_user.id}/hot_videos')
        result = res.data['results'][0]
        self.assertFalse(result['is_paid'])
        self.assertIsNone(result['url'])

        res = self.client3.get(f'/users/{self.test_user.id}/hot_videos')
        result = res.data['results'][0]
        self.assertTrue(result['is_paid'])
        self.assertEqual(result['url'], self.data['url'])


