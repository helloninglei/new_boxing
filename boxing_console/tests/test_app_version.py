# -*- coding:utf-8 -*-
from rest_framework.test import APITestCase
from biz.models import User, AppVersion
from biz.constants import APPVERSION_FUTURE, IOS, ANDROID


class AppVersionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(id=10158, mobile='10187654321', password='p@sSvV0rd',
                                             is_staff=True, is_active=True, is_superuser=True)
        self.client = self.client_class()
        self.client.login(username=self.user, password='p@sSvV0rd')

    def test_app_version_list(self):
        res = self.client.get('/app_versions')
        self.assertEqual(len(res.data['results']), 2)
        self.assertEqual(res.status_code, 200)

    def test_app_version_add(self):
        data = {
            "version": "3.3.1",
            "platform": ANDROID,
            "status": APPVERSION_FUTURE,
            "message": "大扎好，我系渣渣辉，贪玩蓝月，你从味完过的船新版本，是兄弟就来砍我",
            "inner_number": 45,
            "force": False,
            "package": "/path/to/app.apk"
        }
        res = self.client.post('/app_versions', data=data)
        self.assertEqual(res.status_code, 201)
        data = {
            "version": "3.3.1",
            "platform": IOS,
            "status": APPVERSION_FUTURE,
            "message": "大扎好，我系渣渣辉，贪玩蓝月，你从味完过的船新版本，是兄弟就来砍我",
            "force": False,
        }
        res = self.client.post('/app_versions', data=data)
        self.assertEqual(res.status_code, 201)

    def test_app_version_edit(self):
        version_ios = AppVersion.objects.create(version='3.3.2', platform=IOS, message='apple-3-3-2', status=APPVERSION_FUTURE, force=True)
        data = {
            'id': version_ios.id,
            "version": "3.3.3",
            "platform": IOS,
            "status": APPVERSION_FUTURE,
            "message": "apple-3-3-3",
            "force": False,
        }
        res = self.client.patch(f'/app_versions/{version_ios.id}', data=data)
        self.assertEqual(res.status_code, 200)
        version_android = AppVersion.objects.create(version='3.3.2', platform=ANDROID, message='android-3-3-2', inner_number=47,
                                                    package='/path/to/app.apk', status=APPVERSION_FUTURE, force=True)
        data = {
            'id': version_android.id,
            "version": "3.3.3",
            "platform": ANDROID,
            "status": APPVERSION_FUTURE,
            "message": "android-3-3-3",
            "force": False,
            'inner_number': 47,
            'package': '/path/to/new.apk'
        }
        res = self.client.patch(f'/app_versions/{version_android.id}', data=data)
        self.assertEqual(res.status_code, 200)

    def test_app_version_release(self):
        version = AppVersion.objects.create(version='3.3.3', platform=IOS, message='apple-3-3-3', status=APPVERSION_FUTURE, force=True)
        data = {'id': version.id}
        res = self.client.post('/app_release', data=data)
        print(res.data)
        self.assertEqual(res.status_code, 200)
