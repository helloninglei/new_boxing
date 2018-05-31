from rest_framework import status
from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, OfficialAccountChangeLog


class OfficialAccountChangeLogsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(mobile="18800000000", password="password")
        self.client = self.client_class()
        self.client.login(username=self.user.mobile, password="password")

    def test_official_account_change_logs(self):
        data = dict(
            change_amount=10000, related_user=self.user, change_type=constants.OFFICE_ACCOUNT_CHANGE_TYPE_CHOICE[0][0]
        )

        [OfficialAccountChangeLog.objects.create(**data) for _ in range(4)]

        response = self.client.get(path="/official_account_change_logs")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)
        self.assertEqual(response.data['total_count'], 40000)
