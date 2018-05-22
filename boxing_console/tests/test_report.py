# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework import status
from biz import models
from biz.constants import REPORT_REASON_CHOICES, REPORT_STATUS_NOT_PROCESSED, REPORT_STATUS_PROVED_FALSE, \
    REPORT_STATUS_DELETED


class ReportTestCase(APITestCase):
    def setUp(self):
        self.test_user = models.User.objects.create_superuser(mobile='11111111111', password='password')
        self.client = self.client_class()
        self.client.login(username=self.test_user, password='password')

        self.message = models.Message.objects.create(user=self.test_user, content='test content')
        video_data = {
            'user_id': self.test_user.id,
            'name': 'test video1',
            'description': 'test video1',
            'price': 111,
            'url': '/videos/111',
            'try_url': '/videos/222',
            'operator': self.test_user,
        }
        self.hot_video = models.HotVideo.objects.create(**video_data)
        self.report1 = models.Report.objects.create(user=self.test_user, content_object=self.message,
                                                    reason=REPORT_REASON_CHOICES[0][0])
        self.report2 = models.Report.objects.create(user=self.test_user, content_object=self.message,
                                                    reason=REPORT_REASON_CHOICES[0][0])
        self.report3 = models.Report.objects.create(user=self.test_user, content_object=self.hot_video,
                                                    reason=REPORT_REASON_CHOICES[1][0])
        self.report4 = models.Report.objects.create(user=self.test_user, content_object=self.hot_video,
                                                    reason=REPORT_REASON_CHOICES[2][0],
                                                    status=REPORT_STATUS_PROVED_FALSE)

    def test_list(self):
        res = self.client.get('/report', {'status': 'unprocessed'})
        self.assertEqual(res.data['count'], 3)

        res = self.client.get('/report', {'status': 'processed'})
        self.assertEqual(res.data['count'], 1)

    def test_process(self):
        res = self.client.post(f'/report/{self.report1.id}/proved_false')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        report = models.Report.objects.get(pk=self.report1.id)
        self.assertEqual(report.status, REPORT_STATUS_PROVED_FALSE)

        res = self.client.post(f'/report/{self.report2.id}/do_delete')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        report = models.Report.objects.get(pk=self.report2.id)
        self.assertEqual(report.status, REPORT_STATUS_DELETED)
        message = models.Message.all_objects.get(pk=self.message.id)
        self.assertTrue(message.is_deleted)

        res = self.client.post(f'/report/{self.report3.id}/do_delete')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        report = models.Report.objects.get(pk=self.report3.id)
        self.assertEqual(report.status, REPORT_STATUS_DELETED)
        count = models.HotVideo.objects.filter(pk=self.hot_video.id, is_show=True).count()
        self.assertEqual(count, 0)

        res = self.client.get('/report', {'status': 'unprocessed'})
        self.assertEqual(res.data['count'], 0)
