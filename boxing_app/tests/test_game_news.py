# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
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
            "start_time": "2018-12-31 12:59:00",
            "end_time": "2018-12-31 23:59:00",
            "app_content": "分享人生经验",
            "share_content": "人生经验",
            "operator": self.test_user,
        }

    def test_read_count(self):
        news = models.GameNews.objects.create(**self.data)
        res = self.client.get(f'/game_news/{news.id}')
        read_count = res.data['read_count']

        n = 5
        for i in range(n):
            res = self.client.get(f'/game_news/{res.data["id"]}')

        self.assertEqual(read_count + n, res.data['read_count'])

    def test_content(self):
        news = models.GameNews.objects.create(**self.data)
        res = self.client.get(f'/game_news/{news.id}?in_app=1')
        content = res.data['content']
        self.assertEqual(content, self.data['app_content'])

        res = self.client.get(f'/game_news/{news.id}')
        content = res.data['content']
        self.assertEqual(content, self.data['share_content'])
