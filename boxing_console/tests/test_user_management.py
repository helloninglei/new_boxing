from rest_framework.test import APITestCase
from biz.models import User
from rest_framework import status
from biz.constants import USER_TYPE_BOXER, USER_TYPE_CELEBRITY, USER_TYPE_MEDIA, USER_TYPE_MAP


class UserManagementTestCase(APITestCase):
    def setUp(self):
        self.fake_user = User.objects.create_user(mobile='21111111111', password='password')
        self.fake_admin_user = User.objects.create_superuser(
            mobile='11111111112', password='password')
        self.client = self.client_class()
        self.client.login(username=self.fake_admin_user, password='password')

    def test_list(self):
        response = self.client.get(path='/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(len(response.data['results'][1]['user_basic_info']), 9)

    def test_filter(self):
        [User.objects.create_user(mobile=f'1298711111{user_type}', password='password', user_type=user_type) for user_type in
         [USER_TYPE_BOXER, USER_TYPE_CELEBRITY, USER_TYPE_MEDIA]]
        response = self.client.get(path="/users?search=2111")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['mobile'], self.fake_user.mobile)

        response = self.client.get(path=f"/users?user_type={USER_TYPE_CELEBRITY}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['user_type'], USER_TYPE_MAP[USER_TYPE_CELEBRITY])

        response = self.client.get(path=f"/users?user_type={USER_TYPE_BOXER}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['user_type'], USER_TYPE_MAP[USER_TYPE_BOXER])

        response = self.client.get(path=f"/users?user_type={USER_TYPE_MEDIA}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['user_type'], USER_TYPE_MAP[USER_TYPE_MEDIA])

        response = self.client.get(path="/users?user_type=4")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['user_type'], "普通用户")

        response = self.client.get(path="/users")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
