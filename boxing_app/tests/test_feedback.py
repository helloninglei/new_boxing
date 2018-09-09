from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from biz.models import User


class Feedback(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(mobile='11111111111', password='password')
        self.client1 = self.client_class()
        self.client1.login(username=self.test_user_1, password='password')

    def test_create_feedback_success(self):
        feedback_data = {
            "content": "我要进行意见反馈",
            "images": ["image001.png",
                       "image002.png",
                       "image003.png",
                       "image004.png",
                       "image005.png",
                       "image006.png",
                       "image007.png",
                       "image008.png"]
        }
        res = self.client1.post(reverse('create_feedback'), data=feedback_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_feedback_fail_because_more_than_8_images(self):
        feedback_data = {
            "content": "我要进行意见反馈",
            "images": ["image001.png",
                       "image002.png",
                       "image003.png",
                       "image004.png",
                       "image005.png",
                       "image006.png",
                       "image007.png",
                       "image008.png",
                       "image009.png",
                       ]
        }
        res = self.client1.post(reverse('create_feedback'), data=feedback_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


