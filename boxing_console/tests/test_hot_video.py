# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from biz import constants
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User, HotVideo, PayOrder
from biz.services.pay_service import PayService
from biz.constants import HOT_VIDEO_USER_ID, HOT_VIDEO_TAG_CHOICES


class HotVideoTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_superuser(mobile='11111111111', password='password')
        self.test_superuser = User.objects.create_superuser(mobile='11111111112', password='password')
        self.test_user3 = User.objects.create_superuser(mobile='11111111113', password='password')
        self.hot_video_user = User.objects.create(id=HOT_VIDEO_USER_ID, mobile='11111111114', password='password')
        self.client1 = self.client_class()
        self.client2 = self.client_class()
        self.client3 = self.client_class()
        self.client1.login(username=self.test_user, password='password')
        self.client2.login(username=self.test_superuser, password='password')
        self.client3.login(username=self.test_user3, password='password')

        self.data = {
            'name': 'test video',
            'description': 'test video',
            'price': 111,
            'url': '/videos/111',
            'try_url': '/videos/222',
            'cover': '/videos/333',
            'users': [self.test_user.id],
            'tag': HOT_VIDEO_TAG_CHOICES[-1][0],
            "push_hot_video": False,
            "start_time": datetime.now() + timedelta(days=1),
            "end_time": datetime.now() + timedelta(days=2),
        }

    def test_create(self):
        res = self.client2.post('/hot_videos', self.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['user_list'][0]['id'], self.test_user.id)
        self.assertEqual(res.data['tag'], self.data['tag'])

        not_exists_user_id = User.objects.all().order_by('-id').first().id + 1
        self.data['users'] = [not_exists_user_id]
        res = self.client2.post('/hot_videos', self.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.data['users'] = [self.test_user.id]
        self.data['push_to_hotvideo'] = True
        res = self.client2.post('/hot_videos', self.data)
        self.assertEqual(len(res.data['user_list']), 2)
        self.assertIn(HOT_VIDEO_USER_ID, [i['id'] for i in res.data['user_list']])

        del self.data['tag']
        res = self.client2.post('/hot_videos', self.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_push(self):
        self.data['start_time'] = datetime.now() - timedelta(days=1)
        self.data['push_hot_video'] = True
        res = self.client1.post('/hot_videos', self.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'][0], '????????????????????????????????????')

        self.data['start_time'] = datetime.now() + timedelta(days=8)
        res = self.client1.post('/hot_videos', self.data)
        self.assertEqual(res.data['message'][0], '??????????????????????????????')

        self.data['start_time'] = datetime.now() + timedelta(days=2)
        res = self.client1.post('/hot_videos', self.data)
        self.assertEqual(res.data['message'][0], '????????????????????????????????????')

        self.data['end_time'] = self.data['start_time'] + timedelta(days=15)
        res = self.client1.post('/hot_videos', self.data)
        self.assertEqual(res.data['message'][0], '??????????????????????????????????????????14??????')

    def test_update(self):
        res = self.client2.post('/hot_videos', self.data)
        video_id = res.data['id']

        new_name = 'new_name'
        self.data['name'] = new_name
        self.client2.put(f'/hot_videos/{video_id}', self.data)
        video = HotVideo.objects.get(pk=video_id)
        self.assertEqual(video.name, new_name)

    def test_list_search(self):
        self.client2.post('/hot_videos', self.data)

        self.data['users'] = [self.test_user3.id]
        self.client2.post('/hot_videos', self.data)

        # list
        res = self.client2.get('/hot_videos')
        self.assertEqual(res.data['count'], 2)

        # search by user_id
        res = self.client2.get(f'/hot_videos?search={self.test_user.id}')
        self.assertEqual(res.data['count'], 1)

        res = self.client2.get(f'/hot_videos?search={self.test_user3.id}')
        self.assertEqual(res.data['count'], 1)

        most_early_date = HotVideo.objects.all().order_by('created_time').first().created_time
        most_late_date = HotVideo.objects.all().order_by('-created_time').first().created_time

        delta = timedelta(days=1)
        date_format = settings.REST_FRAMEWORK['DATETIME_FORMAT']

        start_date = (most_early_date - delta).strftime(date_format)
        end_date = (most_late_date + delta).strftime(date_format)

        # search by name
        res = self.client2.get(f'/hot_videos?search={self.data["name"]}')
        self.assertEqual(res.data['count'], 2)
        res = self.client2.get(f'/hot_videos?search={self.data["name"]}xx')
        self.assertEqual(res.data['count'], 0)

        # filter by date
        res = self.client2.get(f'/hot_videos?start_time={start_date}&end_time={end_date}')
        self.assertEqual(res.data['count'], 2)

        res = self.client2.get(f'/hot_videos?start_time={end_date}')
        self.assertEqual(res.data['count'], 0)

        res = self.client2.get(f'/hot_videos?end_time={start_date}')
        self.assertEqual(res.data['count'], 0)

    def test_video_order(self):
        res = self.client2.post('/hot_videos', self.data)
        video_id = res.data['id']

        video = HotVideo.objects.get(pk=video_id)
        PayOrder.objects.create(
            user=self.test_superuser,
            status=constants.PAYMENT_STATUS_PAID,
            content_object=video,
            amount=video.price,
            out_trade_no=PayService.generate_out_trade_no(),
            payment_type=constants.PAYMENT_TYPE_ALIPAY,
            device=constants.DEVICE_PLATFORM_IOS,
            pay_time=datetime.now()
        )
        PayOrder.objects.create(
            user=self.test_user3,
            status=constants.PAYMENT_STATUS_PAID,
            content_object=video,
            amount=video.price,
            out_trade_no=PayService.generate_out_trade_no(),
            payment_type=constants.PAYMENT_TYPE_ALIPAY,
            device=constants.DEVICE_PLATFORM_IOS,
            pay_time=datetime.now()
        )

        PayOrder.objects.create(
            user=self.test_user,
            status=constants.PAYMENT_STATUS_UNPAID,
            content_object=video,
            out_trade_no=PayService.generate_out_trade_no(),
            payment_type=constants.PAYMENT_TYPE_ALIPAY,
            device=constants.DEVICE_PLATFORM_IOS,
            amount=video.price,
        )

        res = self.client2.get('/hot_videos')
        result = res.data['results'][0]
        self.assertEqual(result['sales_count'], 2)
        self.assertEqual(result['price_amount'], video.price * 2)

    def test_filter(self):
        self.data['users'] = [self.hot_video_user.id]
        self.data['price'] = 0
        self.client2.post('/hot_videos', self.data)

        self.data['users'] = [self.test_user3.id]
        self.data['price'] = 100
        self.client2.post('/hot_videos', self.data)
        self.client2.post('/hot_videos', self.data)

        # list
        res = self.client2.get('/hot_videos')
        self.assertEqual(res.data['count'], 3)

        # is_hot
        res = self.client2.get('/hot_videos?is_hot=all')
        self.assertEqual(res.data['count'], 3)

        res = self.client2.get('/hot_videos?is_hot=yes')
        self.assertEqual(res.data['count'], 1)

        res = self.client2.get('/hot_videos?is_hot=no')
        self.assertEqual(res.data['count'], 2)

        # is_need_pay
        res = self.client2.get('/hot_videos?is_need_pay=all')
        self.assertEqual(res.data['count'], 3)

        res = self.client2.get('/hot_videos?is_need_pay=yes')
        self.assertEqual(res.data['count'], 2)

        res = self.client2.get('/hot_videos?is_need_pay=no')
        self.assertEqual(res.data['count'], 1)
