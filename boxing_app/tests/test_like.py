# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework import status

from biz import constants, models
from biz.models import User, Message
from biz.redis_client import unlike_hot_video


class LikeTestCase(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(mobile='11111111111', password='password')
        self.test_user_2 = User.objects.create_user(mobile='11111111112', password='password')
        self.test_user_3 = User.objects.create_user(mobile='11111111113', password='password')
        self.client1 = self.client_class()
        self.client1.login(username=self.test_user_1, password='password')
        self.client2 = self.client_class()
        self.client2.login(username=self.test_user_2, password='password')
        self.client3 = self.client_class()
        self.client3.login(username=self.test_user_3, password='password')

    def prepare(self):
        msg_data = {'content': 'message1'}
        res = self.client1.post('/messages', msg_data)
        self.message_id1 = res.data['id']

        res = self.client1.post('/messages', msg_data)
        self.message_id2 = res.data['id']

        res = self.client1.post('/messages', msg_data)
        self.message_id3 = res.data['id']

    def test_create_like(self):
        self.prepare()
        res = self.client1.post(f'/messages/{self.message_id2}/like')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        response = self.client1.get('/messages')

        for message in response.data['results']:
            is_like = message['is_like']
            like_count = message['like_count']
            if message['id'] == self.message_id2:
                self.assertTrue(is_like)
                self.assertEqual(like_count, 1)
            else:
                self.assertFalse(is_like)
                self.assertEqual(like_count, 0)

        response = self.client2.get('/messages')
        for message in response.data['results']:
            is_like = message['is_like']
            like_count = message['like_count']
            self.assertFalse(is_like)
            if message['id'] == self.message_id2:
                self.assertEqual(like_count, 1)
            else:
                self.assertEqual(like_count, 0)

        initial_like_count = 10
        Message.objects.update(initial_like_count=initial_like_count)
        response = self.client2.get('/messages')
        for message in response.data['results']:
            is_like = message['is_like']
            like_count = message['like_count']
            self.assertFalse(is_like)
            if message['id'] == self.message_id2:
                self.assertEqual(like_count, 1 + initial_like_count)
            else:
                self.assertEqual(like_count, 0 + initial_like_count)

    def test_hot_message(self):
        self.prepare()
        self.client1.post('/messages/%s/like' % self.message_id1)
        self.client1.post('/messages/%s/like' % self.message_id2)
        self.client2.post('/messages/%s/like' % self.message_id2)
        self.client3.post('/messages/%s/like' % self.message_id2)
        self.client2.post('/messages/%s/like' % self.message_id3)

        response = self.client1.get('/messages/hot')
        last_count = None
        for message in response.data['results']:
            like_count = message['like_count']
            if last_count is None:
                last_count = like_count
            self.assertGreaterEqual(last_count, like_count)
            last_count = like_count

        msg = Message.objects.get(pk=self.message_id3)
        msg.initial_like_count = 1000
        msg.save()
        response = self.client1.get('/messages/hot')
        self.assertEqual(response.data['results'][0]['id'], self.message_id3)
        response = self.client1.get(f'/messages/{self.message_id3}')
        self.assertEqual(response.data['like_count'], 1 + 1000)

    def test_unset_like(self):
        self.prepare()
        self.client1.post('/message/%s/like/' % self.message_id2)
        self.client1.delete('/message/%s/like/' % self.message_id2)
        response = self.client1.get('/messages')
        for message in response.data['results']:
            is_like = message['is_like']
            self.assertFalse(is_like)

    def test_like_me_list(self):
        self.prepare()
        self.client1.post('/messages/%s/like' % self.message_id1)
        self.client1.post('/messages/%s/like' % self.message_id2)
        self.client2.post('/messages/%s/like' % self.message_id2)
        self.client3.post('/messages/%s/like' % self.message_id3)

        # has unread like list
        response = self.client1.get(path="/unread_like_comment")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['has_unread_comment'])
        self.assertTrue(response.data['has_unread_like'])

        # read like list
        response = self.client1.get('/like_me')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)

        # not has unread like list
        response = self.client1.get(path="/unread_like_comment")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['has_unread_like'])
        self.assertFalse(response.data['has_unread_comment'])

    def test_like_hot_video(self):
        data = {
            'name': 'test video1',
            'description': 'test video1',
            'price': 111,
            'url': '/videos/111',
            'try_url': '/videos/222',
            'operator_id': self.test_user_1.id,
            'cover': '/videos/333',
            "push_hot_video": False,
            "tag": constants.HOT_VIDEO_TAG_DEFAULT,
        }

        video = models.HotVideo.objects.create(**data)
        video.users.add(self.test_user_1.id)

        res = self.client1.get(f'/users/{self.test_user_1.id}/hot_videos/{video.id}')
        self.assertFalse(res.data['is_like'])

        self.client1.post(f'/hot_videos/{video.id}/like')
        res = self.client1.get(f'/users/{self.test_user_1.id}/hot_videos/{video.id}')
        self.assertTrue(res.data['is_like'])

        unlike_hot_video(self.test_user_1.id, video.id)
