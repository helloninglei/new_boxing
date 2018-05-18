from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, BoxerIdentification, Course, PayOrder, UserProfile


class CourseOrderTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(mobile='11111111111', password='password')
        self.client = self.client_class()
        self.client.login(username=self.user1, password='password')
        self.user_profile_data = {
            "user": self.user1,
            "nick_name": "赵柳"
        }
        self.boxer_data = {
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
        self.course_data = {
            "boxer": None,
            "course_name": constants.BOXER_ALLOWED_COURSES_MMA,
            "price": 100,
            "duration": 120,
            "validity": "2018-08-25"
        }
        self.course_order_data = {
            "user": self.user1,
            "content_object": None,
            "status": constants.PAYMENT_STATUS_WAIT_USE,
            "out_trade_no": 111111111,
            "payment_type": constants.PAYMENT_TYPE_WALLET,
            "amount": 100000,
            "device": 1,
            "pay_time": datetime.now()
        }
        self.other_order_data = {
            "user": self.user1,
            "content_object": self.user1,
            "status": constants.PAYMENT_STATUS_WAIT_USE,
            "out_trade_no": 111111111,
            "payment_type": constants.PAYMENT_TYPE_WALLET,
            "amount": 100000,
            "device": 1,
            "pay_time": datetime.now()
        }

    def test_course_order_list(self):
        # 创建user_profile->创建boxer->创建course->创建course_order
        UserProfile.objects.create(**self.user_profile_data)
        boxer = BoxerIdentification.objects.create(**self.boxer_data)
        self.course_data['boxer'] = boxer
        course = Course.objects.create(**self.course_data)
        self.course_order_data['content_object'] = course

        PayOrder.objects.create(**self.course_order_data)
        PayOrder.objects.create(**self.course_order_data)
        PayOrder.objects.create(**self.other_order_data)

        # 只返回课程相关的订单
        res = self.client.get('/course/orders')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

        # 通过用户手机号搜索
        search_user_mobile_res = self.client.get('/course/orders', {"search": self.other_order_data['user']})
        self.assertEqual(search_user_mobile_res.data['count'], 2)
        search_user_mobile_res = self.client.get('/course/orders', {"search": 12222222222})
        self.assertEqual(search_user_mobile_res.data['count'], 0)

        # 通过拳手姓名搜索
        search_user_mobile_res = self.client.get('/course/orders', {"search": self.boxer_data['real_name']})
        self.assertEqual(search_user_mobile_res.data['count'], 2)
        search_user_mobile_res = self.client.get('/course/orders', {"search": "你是谁"})
        self.assertEqual(search_user_mobile_res.data['count'], 0)

        # 通过拳手手机号搜索
        search_user_mobile_res = self.client.get('/course/orders', {"search": self.boxer_data['mobile']})
        self.assertEqual(search_user_mobile_res.data['count'], 2)
        search_user_mobile_res = self.client.get('/course/orders', {"search": 12222222222})
        self.assertEqual(search_user_mobile_res.data['count'], 0)

        # 通过大于等于支付时间过滤
        search_order_time_res = self.client.get('/course/orders', {
            "pay_time_start": self.other_order_data['pay_time'].strftime('%Y-%m-%d %H:%M:%S')})
        self.assertEqual(search_order_time_res.data['count'], 2)
        search_order_time_res = self.client.get('/course/orders', {
            "pay_time_start": (self.other_order_data['pay_time'] + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')})
        self.assertEqual(search_order_time_res.data['count'], 0)

        # 通过小于等于支付时间过滤
        search_order_time_res = self.client.get('/course/orders', {
            "pay_time_end": (self.other_order_data['pay_time'] + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')})
        self.assertEqual(search_order_time_res.data['count'], 2)
        search_order_time_res = self.client.get('/course/orders', {
            "pay_time_end": (self.other_order_data['pay_time'] - timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')})
        self.assertEqual(search_order_time_res.data['count'], 0)

        # 通过课程名过滤
        search_user_mobile_res = self.client.get('/course/orders', {
            "course__course_name": self.course_data['course_name']})
        self.assertEqual(search_user_mobile_res.data['count'], 2)
        search_user_mobile_res = self.client.get('/course/orders', {"course__course_name": "unkonw_course"})
        self.assertEqual(search_user_mobile_res.data['count'], 0)

        # 通过支付方式过滤
        search_user_mobile_res = self.client.get('/course/orders', {
            "payment_type": self.other_order_data['payment_type']})
        self.assertEqual(search_user_mobile_res.data['count'], 2)
        search_user_mobile_res = self.client.get('/course/orders', {"payment_type": "unknown_type"})
        self.assertEqual(search_user_mobile_res.data['count'], 0)

        # 通过订单状态过滤
        search_user_mobile_res = self.client.get('/course/orders', {"status": self.other_order_data['status']})
        self.assertEqual(search_user_mobile_res.data['count'], 2)
        search_user_mobile_res = self.client.get('/course/orders', {"status": "unknown_status"})
        self.assertEqual(search_user_mobile_res.data['count'], 0)

    def test_course_detail(self):
        # 创建user_profile->创建boxer->创建course->创建course_order
        UserProfile.objects.create(**self.user_profile_data)
        boxer = BoxerIdentification.objects.create(**self.boxer_data)
        self.course_data['boxer'] = boxer
        course = Course.objects.create(**self.course_data)
        self.course_order_data['content_object'] = course

        course_order = PayOrder.objects.create(**self.course_order_data)
        res = self.client.get(f'/course/order/{course_order.pk}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        for key in self.course_order_data.keys():
            if key == 'user':
                self.assertEqual(self.course_order_data[key], User.objects.get(pk=res.data['user_id']))
            elif key == 'content_object':
                self.assertEqual(self.course_order_data[key], Course.objects.get(pk=res.data['object_id']))
            elif key == 'device':
                pass
            elif key == 'pay_time':
                self.assertEqual(self.course_order_data[key].strftime('%Y-%m-%d %H:%M:%S'), res.data.get(key))
            else:
                self.assertEqual(self.course_order_data[key], res.data.get(key))