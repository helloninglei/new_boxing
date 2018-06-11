from rest_framework.test import APITestCase
from biz.models import User, UserProfile


class CreateSuperUserTestCase(APITestCase):
    def test_create_superuser(self):
        user = User.objects.create_superuser(mobile="16677777777", password="password")
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
