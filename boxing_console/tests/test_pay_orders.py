from rest_framework import status
from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, PayOrder, HotVideo, Course, BoxerIdentification


class PayOrderTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(mobile="19800000000", password="password")
        self.client = self.client_class()
        self.client.login(username=self.user.mobile, password="password")

    def test_pay_orders_list(self):
        hot_video_data = {
            'user': self.user,
            'name': 'test video1',
            'description': 'test video1',
            'price': 111,
            'url': '/videos/111',
            'try_url': '/videos/222',
            'operator': self.user,
        }
        hot_video = HotVideo.objects.create(**hot_video_data)

        boxer_data = {
            "user": self.user,
            "real_name": "张三",
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "131313141444141444",
            "mobile": "11313131344",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "job": 'hhh',
            "introduction": "beautiful",
            "experience": '',
            "honor_certificate_images": ['http://img1.com', 'http://img2.com', 'http://img3.com'],
            "competition_video": 'https://baidu.com'
        }
        course_data = {
            "boxer": BoxerIdentification.objects.create(**boxer_data),
            "course_name": constants.BOXER_ALLOWED_COURSES_MMA,
            "price": 100,
            "duration": 120,
            "validity": "2018-08-25",
            "club": None
        }
        course = Course.objects.create(**course_data)
        out_trade_no_yield = (num for num in range(2))
        pay_order_partial_data = dict(
            user=self.user, out_trade_no=next(out_trade_no_yield), amount=20000, device=1,
        )

        PayOrder.objects.create(**pay_order_partial_data, content_object=hot_video)
        PayOrder.objects.create(**pay_order_partial_data, content_object=course)

        # 请求列表
        response = self.client.get(path="/pay_orders")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        # search
        response = self.client.get(path="/pay_orders", data={"search": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        # filter
        response = self.client.get(path="/pay_orders", data={"search": 1, "status": 1, "payment_type": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

        response = self.client.get(path="/pay_orders", data={"search": 1, "status": 1, "device": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
