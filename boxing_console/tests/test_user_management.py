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
        self.assertEqual(len(response.data['results'][1]['user_basic_info']), 9)

    def test_filter(self):
        response = self.client.get(path="/users?search=2111")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['mobile'], self.fake_user.mobile)

        response = self.client.get(path="/users?is_boxer=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data['results'], [])

        response = self.client.get(path="/users?is_boxer=false")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(len(response.data['results'][1]['user_basic_info']), 9)
