from rest_framework.test import APITestCase
from django.conf import settings
from rest_framework import status
from biz.models import User


class VersionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(mobile="19909999999", password="password")
        self.client = self.client_class()
        self.client.login(username=self.user.mobile, password="password")

    def test_version(self):
        # ios
        self.client.credentials(source="ios")
        response = self.client.get(path="/version")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, settings.IOS_VERSION)

        # android
        self.client.credentials(source="android")
        response = self.client.get(path="/version")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, settings.ANDROID_VERSION)
