from rest_framework.test import APITestCase

from biz.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(mobile='11111111111', password='password')
        self.client = self.client_class()
        self.client.login(username=self.user1, password='password')
