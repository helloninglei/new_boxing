# -*- coding: utf-8 -*-
from biz import constants
from rest_framework.test import APITestCase
from rest_framework import status
from biz import models


class BannerTestCase(APITestCase):
    def setUp(self):
        self.test_user = models.User.objects.create_superuser(mobile='11111111111', password='password')
        self.client = self.client_class()
        self.client.login(username=self.test_user, password='password')

        news_data = {
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
        self.game_news = models.GameNews.objects.create(**news_data)

        hot_video_data = {
            'name': 'test video1',
            'description': 'test video1',
            'price': 111,
            'url': '/videos/111',
            'try_url': '/videos/222',
            'cover': '/videos/333',
            'users': [self.test_user.id],
        }

        self.client.post('/hot_videos', hot_video_data)
        self.hot_video = models.HotVideo.objects.first()

    def test_create(self):
        # url 格式不合法
        invalid_link_data = {
            'name': 'test banner',
            'order_number': 100,
            'link_type': constants.BANNER_LINK_TYPE_IN_APP_WEB,
            'link': 'invalid_link',
            'picture': '/banners',
        }

        res = self.client.post('/banners', invalid_link_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'][0], "请输入合法的URL。")

        #  链接格式错误
        invalid_link_data = {
            'name': 'test banner',
            'order_number': 100,
            'link_type': constants.BANNER_LINK_TYPE_IN_APP_NATIVE,
            'link': 'invalid_link',
            'picture': '/banners',
        }

        res = self.client.post('/banners', invalid_link_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'][0], '链接格式错误: model_name:obj_id')

        # 未知的链接对象
        invalid_link_data = {
            'name': 'test banner',
            'order_number': 100,
            'link_type': constants.BANNER_LINK_TYPE_IN_APP_NATIVE,
            'link': 'invalid_model:1',
            'picture': '/banners',
        }

        res = self.client.post('/banners', invalid_link_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'][0], '未知的链接对象')

        # 链接对象不存在
        invalid_link_data = {
            'name': 'test banner',
            'order_number': 100,
            'link_type': constants.BANNER_LINK_TYPE_IN_APP_NATIVE,
            'link': f'game_news:{self.game_news.id+1}',
            'picture': '/banners',
        }

        res = self.client.post('/banners', invalid_link_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'][0], f'赛事资讯:{self.game_news.id+1} 不存在')

        # 成功
        valid_link_data = {
            'name': 'test banner',
            'order_number': 100,
            'link_type': constants.BANNER_LINK_TYPE_IN_APP_NATIVE,
            'link': f'game_news:{self.game_news.id}',
            'picture': '/banners',
        }

        res = self.client.post('/banners', valid_link_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        valid_link_data = {
            'name': 'test banner',
            'order_number': 10,
            'link_type': constants.BANNER_LINK_TYPE_IN_APP_NATIVE,
            'link': f'hot_video:{self.hot_video.id}',
            'picture': '/banners',
        }

        res = self.client.post('/banners', valid_link_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.post('/banners', valid_link_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'][0], '序号已存在')

    def test_list_search(self):
        valid_link_data = {
            'name': 'test banner 1',
            'order_number': 100,
            'link_type': constants.BANNER_LINK_TYPE_IN_APP_NATIVE,
            'link': f'game_news:{self.game_news.id}',
            'picture': '/banners',
        }
        self.client.post('/banners', valid_link_data)

        valid_link_data['name'] = 'test banner 2'
        valid_link_data['order_number'] = 101
        self.client.post('/banners', valid_link_data)

        valid_link_data['name'] = 'test banner 3'
        valid_link_data['order_number'] = 102
        self.client.post('/banners', valid_link_data)

        res = self.client.get('/banners', {'search': 'test banner'})
        print(res.data)
        self.assertEqual(res.data['count'], 3)

        res = self.client.get('/banners', {'search': 'test banner 1'})
        self.assertEqual(res.data['count'], 1)

        res = self.client.get('/banners', {'search': 'test banner 4'})
        self.assertEqual(res.data['count'], 0)

    def test_list_order(self):
        valid_link_data = {
            'name': 'test banner 1',
            'order_number': 100,
            'link_type': constants.BANNER_LINK_TYPE_IN_APP_NATIVE,
            'link': f'game_news:{self.game_news.id}',
            'picture': '/banners',
        }
        banner1 = self.client.post('/banners', valid_link_data).data

        valid_link_data['order_number'] = 200
        banner2 = self.client.post('/banners', valid_link_data).data

        valid_link_data['order_number'] = 10
        banner3 = self.client.post('/banners', valid_link_data).data

        banners = self.client.get('/banners').data['results']

        self.assertEqual(banners[0]['id'], banner2['id'])
        self.assertEqual(banners[1]['id'], banner1['id'])
        self.assertEqual(banners[2]['id'], banner3['id'])
