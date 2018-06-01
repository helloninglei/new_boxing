# -*- coding: utf-8 -*-
from biz import constants
from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User
from biz.redis_client import redis_client


class MessageTestCase(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(mobile='11111111111', password='password')
        self.test_user_2 = User.objects.create_user(mobile='11111111112', password='password')
        self.test_user_3 = User.objects.create_user(mobile='11111111113', password='password')
        self.test_user_4 = User.objects.create_user(mobile='11111111114', password='password')
        self.client1 = self.client_class()
        self.client2 = self.client_class()
        self.client3 = self.client_class()
        self.client4 = self.client_class()
        self.client1.login(username=self.test_user_1, password='password')
        self.client2.login(username=self.test_user_2, password='password')
        self.client3.login(username=self.test_user_3, password='password')
        self.client4.login(username=self.test_user_4, password='password')
        self.anonymous_client = self.client_class()

        redis_client.flushdb()

    def test_create_failed(self):
        msg1 = {'content': 'hello2', 'images': ['http://img1.com', 'http://img2.com'], 'video': '/uploads/xxx.jpg'}
        res = self.client1.post('/messages', msg1)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['video'][0], '视频和图片不可同时上传')

        msg1 = {'content': '', 'images': [], 'video': ''}
        res = self.client1.post('/messages', msg1)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'][0], '文字、图片、视频需要至少提供一个')

    def test_create(self):
        msg1 = {'content': 'hello1'}
        msg2 = {'images': ['http://img1.com', 'http://img2.com']}
        self.client1.post('/messages', msg1)
        self.client1.post('/messages', msg2)

        response = self.client1.get(path='/messages')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        results = response.data['results']
        self.assertEqual(msg1['content'], results[1]['content'])
        self.assertEqual(msg2['images'], results[0]['images'])

    def test_msg_type(self):
        msg1 = {'content': 'hello1'}
        msg2 = {'content': 'hello2', 'images': ['http://img1.com', 'http://img2.com']}
        msg3 = {'content': 'hello2', 'video': '/uploads/xxx.mp4'}
        res = self.client1.post('/messages', msg1)
        self.assertEqual(res.data['msg_type'], constants.MESSAGE_TYPE_ONLY_TEXT)

        res = self.client1.post('/messages', msg2)
        self.assertEqual(res.data['msg_type'], constants.MESSAGE_TYPE_HAS_IMAGE)

        res = self.client1.post('/messages', msg3)
        self.assertEqual(res.data['msg_type'], constants.MESSAGE_TYPE_HAS_VIDEO)

    def test_delete(self):
        res = self.client1.post('/messages', {'content': 'hello'})
        client_1_message_id = res.data['id']
        self.client1.post('/messages', {'content': 'hello', 'images': ['http://img1.com', 'http://img2.com']})
        self.client2.post('/messages', {'content': 'hello'})

        res = self.client2.delete('/messages/%s' % client_1_message_id)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client1.delete('/messages/%s' % client_1_message_id)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client1.get(path='/messages')
        self.assertEqual(len(response.data['results']), 2)

    def prepare(self):
        msg = {'content': 'hello1'}
        self.client1.post('/messages', msg)

        self.client2.post('/messages', msg)
        self.client2.post('/messages', msg)
        self.client3.post('/messages', msg)

        self.client4.post('/messages', msg)

    def test_following_and_user_messages(self):
        self.prepare()
        self.client1.post('/follow', {'user_id': self.test_user_2.id})
        self.client1.post('/follow', {'user_id': self.test_user_3.id})

        # following
        res = self.client1.get('/messages/following')
        result = res.data['results']
        self.assertEqual(len(result), 3)
        following_user_ids = [self.test_user_2.id, self.test_user_3.id]
        for message in result:
            self.assertIn(message['user']['id'], following_user_ids)

        # mine
        res = self.client1.get('/messages/mine')
        result = res.data['results']
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['user']['id'], self.test_user_1.id)

        # user
        res = self.client1.get(f'/messages?user_id={self.test_user_2.id}')
        result = res.data['results']
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['user']['id'], self.test_user_2.id)

    def test_permissions(self):
        self.prepare()
        res = self.anonymous_client.get('/messages')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 5)

        msg = {'content': 'hello1'}
        res = self.anonymous_client.post('/messages', msg)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
