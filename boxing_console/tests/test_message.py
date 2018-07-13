# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User, Message


class MessageTestCase(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_superuser(mobile='11111111111', password='password')
        self.client1 = self.client_class()
        self.client1.login(username=self.test_user_1, password='password')

    def prepare(self):
        msg = {'content': 'hello1', 'user': self.test_user_1}
        self.message = Message.objects.create(**msg)

    def test_messages(self):
        self.prepare()
        res = self.client1.get(f'/messages/{self.message.id}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        initial_like_count = 10
        self.client1.patch(f'/messages/{self.message.id}',
                   {'initial_like_count': initial_like_count, 'initial_forward_count': initial_like_count})

        res = self.client1.get(f'/messages/{self.message.id}')
        self.assertEqual(res.data['initial_like_count'], initial_like_count)
        self.assertEqual(res.data['initial_forward_count'], initial_like_count)

