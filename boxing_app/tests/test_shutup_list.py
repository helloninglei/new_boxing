from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User


class ShutUpListTestCase(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user = User.objects.create_user(mobile="12345609099", password="password")
        self.client.login(username=self.user.mobile, password="password")
        self.user2 = User.objects.create_user(mobile="12345609010", password="password")

    def test_shutup_list(self):
        response = self.client.post(path="/shutup_list", data={"user_ids": [self.user2.id]})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(path="/shutup_list")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data['results'], [str(self.user2.id)])

        response = self.client.post(path="/shutup_list_delete", data={"user_ids": [self.user2.id]})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(path="/shutup_list")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
