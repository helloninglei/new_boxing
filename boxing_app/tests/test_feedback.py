import time

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from biz.models import User
from biz.redis_client import redis_client


class Feedback(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(mobile='11111111111', password='password')
        self.client1 = self.client_class()
        self.client1.login(username=self.test_user_1, password='password')
        redis_client.flushdb()

    def test_create_feedback_success(self):
        redis_client.flushdb()
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
                       "image009.png"]
        }
        res1 = self.client1.post(reverse('create_feedback'), data=feedback_data)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        for key in feedback_data:
            self.assertEqual(res1.data[key], feedback_data[key])
        # limited create feedback 5/day
        res2 = self.client1.post(reverse('create_feedback'), data=feedback_data)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        res3 = self.client1.post(reverse('create_feedback'), data=feedback_data)
        self.assertEqual(res3.status_code, status.HTTP_201_CREATED)
        res4 = self.client1.post(reverse('create_feedback'), data=feedback_data)
        self.assertEqual(res4.status_code, status.HTTP_201_CREATED)
        res5 = self.client1.post(reverse('create_feedback'), data=feedback_data)
        self.assertEqual(res5.status_code, status.HTTP_201_CREATED)
        res6 = self.client1.post(reverse('create_feedback'), data=feedback_data)
        self.assertEqual(res6.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_create_feedback_fail_because_more_than_8_images(self):
        redis_client.flushdb()
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
                       "image010.png",
                       ]
        }
        res = self.client1.post(reverse('create_feedback'), data=feedback_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


