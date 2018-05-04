# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User


class MessageTestCase(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(mobile='11111111111', password='password')
        self.test_user_2 = User.objects.create_user(mobile='11111111112', password='password')
        self.client1 = self.client_class()
        self.client1.login(username=self.test_user_1, password='password')
        self.client2 = self.client_class()
        self.client2.login(username=self.test_user_2, password='password')

    def test_create(self):
        msg1 = {'content': 'hello1'}
        msg2 = {'content': 'hello2', 'images': ['http://img1.com', 'http://img2.com'], 'video': 'https://baidu.com'}
        self.client1.post('/messages', msg1)
        self.client1.post('/messages', msg2)

        response = self.client1.get(path='/messages')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        results = response.data['results']
        self.assertEqual(msg2['content'], results[0]['content'])
        self.assertEqual(msg2['images'], results[0]['images'])
        self.assertEqual(msg2['video'], results[0]['video'])
        self.assertEqual(msg1['content'], results[1]['content'])

    def test_delete(self):
        res = self.client1.post('/messages', {'content': 'hello'})
        client_1_message_id = res.data['id']
        self.client1.post('/messages', {'content': 'hello', 'images': ['http://img1.com', 'http://img2.com'], 'video': 'https://baidu.com'})
        self.client2.post('/messages', {'content': 'hello'})

        res = self.client2.delete('/messages/%s' % client_1_message_id)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client1.delete('/messages/%s' % client_1_message_id)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client1.get(path='/messages')
        self.assertEqual(len(response.data['results']), 2)
