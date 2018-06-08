# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User
from biz.redis_client import redis_client


class FollowTestCase(APITestCase):
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
        redis_client.flushdb()

    def test_follow(self):
        data = {'user_id': self.test_user_2.id}
        res = self.client1.post('/follow', data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        data = {'user_id': self.test_user_1.id}
        res = self.client1.post('/follow', data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow(self):
        data = {'user_id': self.test_user_2.id}
        res = self.client1.post('/follow', data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client1.post('/unfollow', data)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_follow_list(self):
        self.client1.post('/follow', {'user_id': self.test_user_2.id})
        self.client1.post('/follow', {'user_id': self.test_user_3.id})

        self.client2.post('/follow', {'user_id': self.test_user_3.id})

        self.client3.post('/follow', {'user_id': self.test_user_1.id})

        # test follower list
        res = self.client3.get('/follower')
        result = res.data['result']
        self.assertEqual(len(result), 2)

        self.assertEqual(result[0]['id'], self.test_user_2.id)
        self.assertEqual(result[1]['id'], self.test_user_1.id)

        res = self.client1.get('/follower')
        result = res.data['result']
        self.assertEqual(len(result), 1)

        # test following list
        res = self.client1.get('/following')
        result = res.data['result']
        self.assertEqual(len(result), 2)

        res = self.client2.get('/following')
        result = res.data['result']
        self.assertEqual(len(result), 1)

        # test unfollow
        self.client1.post('/unfollow', {'user_id': self.test_user_3.id})
        res = self.client3.get('/follower')
        result = res.data['result']
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], self.test_user_2.id)

        res = self.client1.get('/following')
        result = res.data['result']
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], self.test_user_2.id)

        # test contact list
        response = self.client1.get(path="/contact")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn("index_letter", response.data['results'][0])
