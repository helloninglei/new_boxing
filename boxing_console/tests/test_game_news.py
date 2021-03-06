# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from biz import models


class GameNewsTestCase(APITestCase):
    def setUp(self):
        self.test_user = models.User.objects.create_superuser(mobile='11111111111', password='password')
        self.client = self.client_class()
        self.client.login(username=self.test_user, password='password')

        self.data = {
            "title": "搞个大新闻",
            "sub_title": "闷声发大财",
            "initial_views_count": 666,
            "picture": "/uploads/aa/67/959ce5a33a6984b10e1d44c965b03c84230f.jpg",
            "stay_top": True,
            "push_news": False,
            "start_time": datetime.now() + timedelta(days=1),
            "end_time": datetime.now() + timedelta(days=2),
            "app_content": "分享人生经验",
            "share_content": "人生经验"
        }

    def test_create(self):
        res = self.client.post('/game_news', self.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(f'/game_news/{res.data["id"]}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # test author
        nick_name = 'Lerry'
        models.UserProfile.objects.filter(user=self.test_user).update(nick_name=nick_name)
        self.test_user.refresh_from_db()
        res = self.client.get(f'/game_news/{res.data["id"]}')
        self.assertEqual(res.data['author'], nick_name)

    def test_created_failed(self):
        self.data['start_time'] = datetime.now() - timedelta(days=1)
        self.data['push_news'] = True
        res = self.client.post('/game_news', self.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'][0], '开始时间必须是以后的时间')

        self.data['start_time'] = datetime.now() + timedelta(days=8)
        res = self.client.post('/game_news', self.data)
        self.assertEqual(res.data['message'][0], '开始时间必须是七天内')

        self.data['start_time'] = datetime.now() + timedelta(days=2)
        res = self.client.post('/game_news', self.data)
        self.assertEqual(res.data['message'][0], '结束时间必须大于开始时间')

        self.data['end_time'] = self.data['start_time'] + timedelta(days=15)
        res = self.client.post('/game_news', self.data)
        self.assertEqual(res.data['message'][0], '结束时间必须在开始时间以后的14天内')

    def test_stay_top(self):
        self.client.post('/game_news', self.data)
        self.data['stay_top'] = False
        self.client.post('/game_news', self.data)

        res = self.client.get('/game_news', {'stay_top': 'all'})
        self.assertEqual(res.data['count'], 2)

        res = self.client.get('/game_news', {'stay_top': 'true'})
        self.assertEqual(res.data['count'], 1)

        res = self.client.get('/game_news', {'stay_top': 'false'})
        self.assertEqual(res.data['count'], 1)

    def test_stat(self):
        news = models.GameNews.objects.create(**self.data)
        news.stay_top = True
        news.views_count = 1
        news.save()

        news = models.GameNews.objects.create(**self.data)
        news.stay_top = True
        news.is_show = False
        news.views_count = 5
        news.save()

        news = models.GameNews.objects.create(**self.data)
        news.stay_top = False
        news.is_show = False
        news.views_count = 10
        news.save()

        res = self.client.get('/game_news')
        self.assertEqual(res.data['count'], 3)
        self.assertEqual(res.data['real_views_amount'], 16)

        res = self.client.get('/game_news', {'stay_top': 'true'})
        self.assertEqual(res.data['count'], 2)
        self.assertEqual(res.data['real_views_amount'], 6)

        res = self.client.get('/game_news', {'stay_top': 'true', 'is_show': 'yes'})
        self.assertEqual(res.data['count'], 1)
        self.assertEqual(res.data['real_views_amount'], 1)

