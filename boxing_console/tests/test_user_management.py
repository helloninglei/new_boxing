# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from biz.models import User, UserProfile
from rest_framework import status


class UserManagementTestCase(APITestCase):
    def setUp(self):
        self.fake_user = User.objects.create_user(mobile='21111111111', password='password')
        self.fake_admin_user = User.objects.create_superuser(
            mobile='11111111112', password='password')
        self.user_profile = UserProfile.objects.create(user=self.fake_user)
        self.client = self.client_class()
        self.client.login(username=self.fake_admin_user, password='password')

    def test_list(self):
        response = self.client.get(path='/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(len(response.data['results'][0]['user_basic_info']), 9)
