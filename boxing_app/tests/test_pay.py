# -*- coding: utf-8 -*-
import datetime
from biz import constants
from rest_framework.test import APITestCase
from biz.models import User, HotVideo, PayOrder

class HotVideoTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(mobile='11111111111', password='password')
        self.test_superuser = User.objects.create_superuser(mobile='11111111112', password='password')
        self.client1 = self.client_class(headers={'source': 'iOS'})
        self.client2 = self.client_class()
        self.client1.login(username=self.test_user, password='password')
        self.client2.login(username=self.test_superuser, password='password')

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
        payment_data = {
            'id': video.id,
            'payment_type': constants.PAYMENT_TYPE_ALIPAY,
        }
        self.client1.post('/hot_videos/create_order', payment_data)



