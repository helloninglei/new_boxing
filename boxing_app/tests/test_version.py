from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User, AppVersion
from biz.constants import IOS, ANDROID, APPVERSION_NOW


class VersionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(mobile="19909999999", password="password")
        self.prefix = PKG_URL = 'http://qa.bituquanguan.com'
        self.client = self.client_class()
        self.client.login(username=self.user.mobile, password="password")
        AppVersion.objects.all().delete()
        self.android_version = AppVersion.objects.create(version='3.3.1', platform=ANDROID, status=APPVERSION_NOW,
                                                         message='android-3-3-1', inner_number=1, force=True, package='/path/to/app.apk')
        self.ios_version = AppVersion.objects.create(version='3.3.1', platform=IOS, status=APPVERSION_NOW,  force=True)
        self.android_data = {'version': self.android_version.version,
                             'inner_number': self.android_version.inner_number,
                             'package': self.android_version.package,
                             'message': self.android_version.message,
                             'force': self.android_version.force}
        self.ios_data = {'version': self.ios_version.version,
                         'message': self.ios_version.message,
                         'force': self.ios_version.force}

    def test_version(self):
        # ios
        self.client.credentials(HTTP_SOURCE="ios")
        response = self.client.get(path="/version")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['version'], self.ios_data['version'])
        self.assertEqual(response.data['message'], self.ios_data['message'])
        self.assertEqual(response.data['force'], self.ios_data['force'])

        # android
        self.client.credentials(HTTP_SOURCE="android")
        response = self.client.get(path="/version")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['version'], self.android_data['version'])
        self.assertEqual(response.data['message'], self.android_data['message'])
        self.assertEqual(response.data['force'], self.android_data['force'])
        self.assertEqual(response.data['version_code'], self.android_data['inner_number'])
        self.assertEqual(response.data['url'], self.prefix + self.android_data['package'])

