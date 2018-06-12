from rest_framework.test import APITestCase
from rest_framework import status
from biz.constants import USER_IDENTITY_DICT
from biz.models import User


class OfficialAccountsTestCase(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user = User.objects.create_user(mobile="19999000000", password="password")
        self.client.login(username=self.user.mobile, password="password")

    def test_official_accounts(self):
        response = self.client.get(path="/get_official_accounts_info")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, USER_IDENTITY_DICT)
