from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, BoxerIdentification, Course, PayOrder


class CourseOrderTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(mobile='11111111111', password='password')
        self.client = self.client_class()
        self.client.login(username=self.user1, password='password')
        self.data = {
                        "user": self.user1,
                        "content_object": '',
                        "status": constants.PAYMENT_STATUS_WAIT_PAY,
                        "out_trade_no": 11111112,
                        "payment_type": constants.PAYMENT_TYPE_WALLET,
                        "amount": 122,
                        "pay_time": "2018-05-08 06:13:51",
                        "user_mobile": "11111111111",
                        "course_name": "THAI_BOXING",
                        "boxer_name": "张三",
                        "boxer_mobile": "111111111",
                        "object_id": 2,
                    }

    def test_course_order_list(self):
        boxer_data = {
            "user": self.user1,
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
        boxer = BoxerIdentification.objects.create(**boxer_data)

        course_data = {"boxer": boxer,
                       "course_name": constants.BOXER_ALLOWED_COURSES_MMA,
                       "price": 100,
                       "duration": 120,
                       "validity": "2018-08-25"}
        course = Course.objects.create(**course_data)

        course_order_data = {
            "user": self.user1,
            "content_object": course,
            "status": constants.PAYMENT_STATUS_WAIT_USE,
            "out_trade_no": 111111111,
            "payment_type": constants.PAYMENT_TYPE_WALLET,
            "amount": 100000,
            "device": 1,
            "pay_time": datetime.now()
        }
        other_order_data = {
            "user": self.user1,
            "content_object": self.user1,
            "status": constants.PAYMENT_STATUS_WAIT_USE,
            "out_trade_no": 111111111,
            "payment_type": constants.PAYMENT_TYPE_WALLET,
            "amount": 100000,
            "device": 1,
            "pay_time": datetime.now()
        }

        PayOrder.objects.create(**course_order_data)
        PayOrder.objects.create(**course_order_data)
        PayOrder.objects.create(**other_order_data)

        # 只返回课程相关的订单
        res = self.client.get('/course/orders')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

        # 通过用户手机号搜索
        search_user_mobile_res = self.client.get('/course/orders', {"search": other_order_data['user']})
        self.assertEqual(search_user_mobile_res.data['count'], 2)
        search_user_mobile_res = self.client.get('/course/orders', {"search": 12222222222})
        self.assertEqual(search_user_mobile_res.data['count'], 0)

        # 通过拳手姓名搜索
        search_user_mobile_res = self.client.get('/course/orders', {"search": boxer_data['real_name']})
        self.assertEqual(search_user_mobile_res.data['count'], 2)
        search_user_mobile_res = self.client.get('/course/orders', {"search": "你是谁"})
        self.assertEqual(search_user_mobile_res.data['count'], 0)

        # 通过拳手手机号搜索
        search_user_mobile_res = self.client.get('/course/orders', {"search": boxer_data['mobile']})
        self.assertEqual(search_user_mobile_res.data['count'], 2)
        search_user_mobile_res = self.client.get('/course/orders', {"search": 12222222222})
        self.assertEqual(search_user_mobile_res.data['count'], 0)

        # 通过大于等于支付时间过滤
        search_order_time_res = self.client.get('/course/orders', {
            "pay_time_start": other_order_data['pay_time'].strftime('%Y-%m-%d %H:%M:%S')})
        self.assertEqual(search_order_time_res.data['count'], 2)
        search_order_time_res = self.client.get('/course/orders', {
            "pay_time_start": (other_order_data['pay_time'] + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')})
        self.assertEqual(search_order_time_res.data['count'], 0)

        # 通过小于等于支付时间过滤
        search_order_time_res = self.client.get('/course/orders', {
            "pay_time_end": (other_order_data['pay_time'] + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')})
        self.assertEqual(search_order_time_res.data['count'], 2)
        search_order_time_res = self.client.get('/course/orders', {
            "pay_time_end": (other_order_data['pay_time'] - timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')})
        self.assertEqual(search_order_time_res.data['count'], 0)

        # 通过课程名过滤
        search_user_mobile_res = self.client.get('/course/orders', {"course__course_name": course_data['course_name']})
        self.assertEqual(search_user_mobile_res.data['count'], 2)
        search_user_mobile_res = self.client.get('/course/orders', {"course__course_name": "nukonw_course"})
        self.assertEqual(search_user_mobile_res.data['count'], 0)

        # 通过支付方式过滤
        search_user_mobile_res = self.client.get('/course/orders', {"payment_type": other_order_data['payment_type']})
        self.assertEqual(search_user_mobile_res.data['count'], 2)
        search_user_mobile_res = self.client.get('/course/orders', {"payment_type": "nukonw_type"})
        self.assertEqual(search_user_mobile_res.data['count'], 0)

        # 通过订单状态过滤
        search_user_mobile_res = self.client.get('/course/orders', {"status": other_order_data['status']})
        self.assertEqual(search_user_mobile_res.data['count'], 2)
        search_user_mobile_res = self.client.get('/course/orders', {"status": "nukonw_status"})
        self.assertEqual(search_user_mobile_res.data['count'], 0)
