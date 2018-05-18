# -*- coding: utf-8 -*-
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
            "start_time": "2018-12-31 12:59:00",
            "end_time": "2018-12-31 23:59:00",
            "app_content": "分享人生经验",
            "share_content": "人生经验"
        }

    def test_create(self):
        res = self.client.post('/game_news', self.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(f'/game_news/{res.data["id"]}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        result = res.data
        for k in self.data:
            self.assertEqual(self.data[k], result[k])

        # test author
        self.assertEqual(result['author'], self.test_user.mobile)

        nick_name = 'Lerry'
        models.UserProfile.objects.create(user=self.test_user, nick_name=nick_name)
        res = self.client.get(f'/game_news/{res.data["id"]}')
        self.assertEqual(res.data['author'], nick_name)
