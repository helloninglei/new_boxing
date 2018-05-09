# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User, Report
from biz.constants import REPORT_OBJECT_DICT
from biz.constants import REPORT_REASON_CHOICES
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
            'reason': REPORT_REASON_CHOICES[0][0],
            'object_id': self.message_id,
        }
        res = self.client2.post('/messages/report', data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        obj = Report.objects.get(id=res.data['object_id'])
        self.assertEqual(REPORT_OBJECT_DICT['message'], obj.object_type)

        data = {
            'object_id': self.message_id,
            'reason': DISCOVER_MESSAGE_REPORT_OTHER_REASON
        }

        res = self.client2.post('/messages/report', data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        data['remark'] = 'test'
        res = self.client2.post('/messages/report', data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
