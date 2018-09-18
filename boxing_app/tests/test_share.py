# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework.test import APITestCase
from biz import models
from biz import constants
from biz.redis_client import get_number_of_share

h5_base_url = settings.SHARE_H5_BASE_URL
oss_base_url = settings.OSS_BASE_URL


class ShareTestCase(APITestCase):
    def setUp(self):
        self.test_user = models.User.objects.create_superuser(mobile='11111111111', password='password')
        self.test_user2 = models.User.objects.create_superuser(mobile='11111111112', password='password')
        self.test_player = models.Player.objects.create(user=self.test_user, name='香港记者', mobile='22222222222',
                                                        avatar='/path/to/face.jpg', stamina=88, skill=90, attack=90,
                                                        defence=90, strength=90, willpower=79)

        self.nick_name = 'lerry'
        self.test_user.user_profile.nick_name = self.nick_name
        self.test_user.user_profile.save()
        self.test_user.refresh_from_db()
        self.client = self.client_class()
        self.client.login(username=self.test_user, password='password')

        self.news_data = news_data = {
            "title": "搞个大新闻",
            "sub_title": "闷声发大财",
            "initial_views_count": 666,
            "picture": "/uploads/aa/67/959ce5a33a6984b10e1d44c965b03c84230f.jpg",
            "stay_top": True,
            "push_news": False,
            "start_time": "2018-12-31 12:59:00",
            "end_time": "2018-12-31 23:59:00",
            "app_content": "分享人生经验",
            "share_content": "人生经验",
            "operator": self.test_user,
        }
        self.news = models.GameNews.objects.create(**news_data)

        msg_data = {'content': 'message', 'images': ['/uploads/xxxxxxxx.jpg'], 'user': self.test_user}
        self.msg = models.Message.objects.create(**msg_data)

        msg_data = {'images': ['/uploads/xxxxxxxx.jpg'], 'user': self.test_user}
        self.msg2 = models.Message.objects.create(**msg_data)

        self.video_data = {
            'name': 'test video1',
            'description': 'test video1',
            'price': 111,
            'url': '/videos/111',
            'try_url': '/uploads/xxxxxxxx.mp4',
            'operator': self.test_user,
            'cover': 'http://xxxx',
            "push_hot_video": False,
            "tag": constants.HOT_VIDEO_TAG_DEFAULT,
        }

        self.video = models.HotVideo.objects.create(**self.video_data)
        self.video.users.add(self.test_user)

    def test_share_content(self):
        img_prefix = '?x-oss-process=image/resize,w_120,h_120'

        data = self.client.get(f'/game_news/{self.news.id}/share').data
        self.assertEqual(data['title'], self.news.title)
        self.assertEqual(data['sub_title'], self.news.sub_title)
        self.assertEqual(data['picture'], f'{oss_base_url}{self.news.picture}{img_prefix}')
        self.assertEqual(data['url'], f'{h5_base_url}game_news/{self.news.id}/0')  # 0 不在app内打开

        data = self.client.get(f'/hot_videos/{self.video.id}/share').data
        self.assertEqual(data['title'], self.video.name)
        self.assertEqual(data['sub_title'], f'来自拳城出击的热门视频')
        self.assertEqual(data['picture'], self.video_data['cover'])
        self.assertEqual(data['url'], f'{h5_base_url}hot_videos/{self.test_user.id}/{self.video.id}')

        self.video.users.add(self.test_user2)
        data = self.client.get(f'/hot_videos/{self.video.id}/share?user_id={self.test_user2.id}').data
        self.assertEqual(data['url'], f'{h5_base_url}hot_videos/{self.test_user2.id}/{self.video.id}')

        data = self.client.get(f'/messages/{self.msg.id}/share').data
        self.assertEqual(data['title'], self.msg.content)
        self.assertEqual(data['sub_title'], f'来自拳城出击的{self.nick_name}')
        self.assertIsNone(data['picture'])

        self.assertEqual(data['url'], f'{h5_base_url}messages/{self.msg.id}')

        avatar = '/uploads/xxx.jpg'
        self.test_user.user_profile.avatar = avatar
        self.test_user.user_profile.save()
        data = self.client.get(f'/messages/{self.msg.id}/share').data
        self.test_user.refresh_from_db()
        self.assertEqual(data['sub_title'], '来自拳城出击的lerry')
        self.assertEqual(data['picture'], f'{oss_base_url}{self.test_user.user_profile.avatar}{img_prefix}')

        data = self.client.get(f'/players/{self.test_user.id}/share').data
        self.assertEqual(data['title'], '分享lerry的个人战绩')
        self.assertEqual(data['sub_title'], "已关注: 0,粉丝数: 0")
        self.assertEqual(data['picture'], f'{oss_base_url}{self.test_player.avatar}{img_prefix}')
        self.assertEqual(data['url'], f'{h5_base_url}players/{self.test_user.id}')

    def test_title_content(self):
        self.news_data['title'] = '1' * 14
        news = models.GameNews.objects.create(**self.news_data)

        data = self.client.get(f'/game_news/{news.id}/share').data
        self.assertEqual(data['title'], self.news_data['title'])

        self.news_data['title'] = '1' * 15
        news = models.GameNews.objects.create(**self.news_data)

        data = self.client.get(f'/game_news/{news.id}/share').data
        self.assertEqual(data['title'], self.news_data['title'])

        data = self.client.get(f'/messages/{self.msg2.id}/share').data
        self.assertEqual(data['title'], f'分享{self.nick_name}动态')

    def test_share_count(self):
        count = get_number_of_share(self.test_user.id)
        self.client.get(f'/game_news/{self.news.id}/share')
        new_count = get_number_of_share(self.test_user.id)
        self.assertEqual(count + 1, new_count)
