# -*- coding: utf-8 -*-
import datetime
from biz import constants
from biz.redis_client import redis_client
from rest_framework.test import APITestCase
from biz.models import User, HotVideo, PayOrder
from biz.services.pay_service import PayService


class HotVideoTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(mobile='11111111111', password='password')
        self.test_superuser = User.objects.create_superuser(mobile='11111111112', password='password')
        self.test_hot_video_user = User.objects.create_user(pk=constants.HOT_VIDEO_USER_ID, mobile='11111111113',
                                                            password='password')
        self.client1 = self.client_class()
        self.client2 = self.client_class()
        self.client3 = self.client_class()
        self.client1.login(username=self.test_user, password='password')
        self.client2.login(username=self.test_superuser, password='password')
        self.client3.login(username=self.test_hot_video_user, password='password')

        self.data = {
            'name': 'test video1',
            'description': 'test video1',
            'price': 111,
            'url': '/videos/111',
            'try_url': '/videos/222',
            'operator_id': self.test_superuser.id,
            'cover': '/videos/333',
            "push_hot_video": False,
            "tag": constants.HOT_VIDEO_TAG_DEFAULT,
        }

        redis_client.flushdb()

    def test_hot_videos(self):
        tag0 = constants.HOT_VIDEO_TAG_CHOICES[0][0]
        tag1 = constants.HOT_VIDEO_TAG_CHOICES[1][0]
        tag2 = constants.HOT_VIDEO_TAG_CHOICES[2][0]

        self.data['tag'] = tag0
        video = HotVideo.objects.create(**self.data)
        video.users.set([self.test_user.id, self.test_hot_video_user.id])

        self.data['tag'] = tag0
        video1 = HotVideo.objects.create(**self.data)
        video1.users.add(self.test_user.id)
        video1.users.add(self.test_superuser.id)

        self.data['tag'] = tag1
        video2 = HotVideo.objects.create(**self.data)
        video2.users.add(self.test_hot_video_user.id)

        self.data['tag'] = tag2
        video3 = HotVideo.objects.create(**self.data)
        video3.users.add(self.test_user.id)

        # recommend videos
        res = self.client1.get(f'/users/{self.test_user.id}/hot_videos/{video.id}')
        self.assertEqual(len(res.data['recommend_videos']), 1)  # 推荐同标签的其他视频

        # all video tag
        res = self.client1.get(f'/users/{self.test_user.id}/hot_videos?tag=0')
        self.assertEqual(len(res.data['results']), 3)

        res = self.client1.get(f'/users/{self.test_user.id}/hot_videos?tag={tag0}')
        self.assertEqual(len(res.data['results']), 2)

        # bind user
        res = self.client1.get(f'/users/{self.test_user.id}/hot_videos/{video.id}')
        self.assertEqual(res.data['bind_user']['id'], self.test_user.id)
        self.assertEqual(len(res.data['other_users']), 0)

        res = self.client1.get(f'/users/{self.test_user.id}/hot_videos/{video1.id}')
        self.assertEqual(res.data['bind_user']['id'], self.test_user.id)
        self.assertEqual(len(res.data['other_users']), 1)

        res = self.client1.get(f'/users/{constants.HOT_VIDEO_USER_ID}/hot_videos/{video2.id}')
        self.assertEqual(res.data['bind_user']['id'], constants.HOT_VIDEO_USER_ID)
        self.assertEqual(len(res.data['other_users']), 0)

    def test_video_payment(self):
        video = HotVideo.objects.create(**self.data)
        video.users.add(self.test_user.id)

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
            user=self.test_hot_video_user,
            status=constants.PAYMENT_STATUS_PAID,
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
