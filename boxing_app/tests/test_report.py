# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User
from biz.constants import DISCOVER_MESSAGE_REPORT_CHOICES
from biz.constants import DISCOVER_MESSAGE_REPORT_OTHER_REASON


class LikeTestCase(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(mobile='11111111111', password='password')
        self.test_user_2 = User.objects.create_user(mobile='11111111112', password='password')
        self.test_user_3 = User.objects.create_user(mobile='11111111113', password='password')
        self.client1 = self.client_class()
        self.client1.login(username=self.test_user_1, password='password')
        self.client2 = self.client_class()
        self.client2.login(username=self.test_user_2, password='password')

    def prepare(self):
        msg_data = {'content': 'message1'}
        res = self.client1.post('/messages', msg_data)
        self.message_id = res.data['id']

    def test_create_report(self):
        self.prepare()
        data = {
            'reason': DISCOVER_MESSAGE_REPORT_CHOICES[0][0]
        }
        res = self.client2.post('/messages/%s/report' % self.message_id, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        data = {
            'reason': DISCOVER_MESSAGE_REPORT_OTHER_REASON
        }

        res = self.client2.post('/messages/%s/report' % self.message_id, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        data['remark'] = 'test'
        res = self.client2.post('/messages/%s/report' % self.message_id, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
