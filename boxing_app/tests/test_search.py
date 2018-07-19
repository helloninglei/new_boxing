from rest_framework import status
from rest_framework.test import APITestCase

from biz.models import User, UserProfile, Message, GameNews, HotVideo


class SearchCase(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(mobile='11111111111', password='password')
        self.test_user_2 = User.objects.create_user(mobile='11111111112', password='password')
        self.test_user_3 = User.objects.create_user(mobile='11111111113', password='password')
        self.client1 = self.client_class()
        self.client1.login(username=self.test_user_1, password='password')
        self.client2 = self.client_class()
        self.client2.login(username=self.test_user_2, password='password')
        self.user_profile_data = {
            "gender": True,
            "name": "name",
            "nation": "nation",
            "avatar": "avatar"
        }
        self.news_data = {
            "sub_title": "闷声发大财",
            "initial_views_count": 666,
            "picture": "/uploads/aa/67/959ce5a33a6984b10e1d44c965b03c84230f.jpg",
            "stay_top": True,
            "push_news": False,
            "start_time": "2018-12-31 12:59:00",
            "end_time": "2018-12-31 23:59:00",
            "app_content": "分享人生经验",
            "share_content": "人生经验",
            "operator": self.test_user_1,
        }
        self.video_data = {
            'description': 'test video1',
            'price': 111,
            'url': '/videos/111',
            'try_url': '/videos/222',
            'operator_id': self.test_user_1.id,
            'cover': '/videos/333'
        }

    def test_search_user(self):
        user1_nick_name = "张三"
        user2_nick_name = "李三"
        UserProfile.objects.filter(user=self.test_user_1).update(nick_name=user1_nick_name)
        UserProfile.objects.filter(user=self.test_user_2).update(nick_name=user2_nick_name)

        res = self.client1.get(f'/search/USER?keywords={user1_nick_name}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        res = self.client1.get('/search/USER?keywords=三')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)
        res = self.client1.get('/search/USER?keywords=')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 0)

    def test_search_message(self):
        content1 = '去泰国看人妖'
        content2 = '去新加坡看风景'
        content3 = '去菲律宾玩水'
        Message.objects.create(user=self.test_user_1, content=content1)
        Message.objects.create(user=self.test_user_2, content=content2)
        Message.objects.create(user=self.test_user_3, content=content3)

        res = self.client1.get(f'/search/MESSAGE?keywords={content1}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        res = self.client1.get('/search/MESSAGE?keywords=看')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)
        res = self.client1.get('/search/MESSAGE?keywords=')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 0)

    def test_search_news(self):
        title1 = "不要总想搞大新闻"
        title2 = "就是想搞大事情"
        self.news_data['title'] = title1
        GameNews.objects.create(**self.news_data)
        self.news_data['title'] = title2
        GameNews.objects.create(**self.news_data)
        GameNews.objects.create(**self.news_data)

        res = self.client1.get(f'/search/NEWS?keywords={title1}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        res = self.client1.get('/search/NEWS?keywords=')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 0)

    def test_search_video(self):
        v_name1 = "世界杯法国夺冠"
        v_name2 = "世界杯梅西想早点回家"
        self.video_data['name'] = v_name1
        HotVideo.objects.create(**self.video_data)
        self.video_data['name'] = v_name2
        HotVideo.objects.create(**self.video_data)

        res = self.client1.get(f'/search/VIDEO?keywords={v_name1}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        res = self.client1.get('/search/VIDEO?keywords=世界杯')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)


