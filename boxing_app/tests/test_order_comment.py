import json
from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, UserProfile, BoxerIdentification, BoxingClub, Course, PayOrder


class MessageTestCase(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(mobile='11111111111', password='password')
        self.test_user_2 = User.objects.create_user(mobile='11111111112', password='password')
        self.test_user_3 = User.objects.create_user(mobile='11111111113', password='password')
        self.test_user_4 = User.objects.create_user(mobile='11111111114', password='password')
        self.test_user = None
        self.client1 = self.client_class()
        self.client2 = self.client_class()
        self.client3 = self.client_class()
        self.client4 = self.client_class()
        self.client1.login(username=self.test_user_1, password='password')
        self.client2.login(username=self.test_user_2, password='password')
        self.client3.login(username=self.test_user_3, password='password')
        self.client4.login(username=self.test_user_4, password='password')
        self.user_profile_data = {
            "user": self.test_user_1,
            "nick_name": "赵柳",
            "gender": True,
            "name": "name",
            "nation": "nation",
            "avatar": "avatar"
        }
        self.boxer_data = {
            "user": self.test_user_1,
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
        self.club_data = {
            "name": "club01",
            "address": "club_address",
            "longitude": 111.111111,
            "latitude": 11.111111,
            "phone": 11111111111,
            "opening_hours": "9:00-22:00",
            "images": ["www.baidu.png"],
            "introduction": "club_introduction"
        }
        self.course_data = {
            "boxer": None,
            "course_name": constants.BOXER_ALLOWED_COURSES_MMA,
            "price": 100,
            "duration": 120,
            "validity": "2018-08-25",
            "club": None
        }
        self.course_order_data = {
            "user": self.test_user_1,
            "content_object": None,
            "status": constants.PAYMENT_STATUS_WAIT_USE,
            "out_trade_no": 111111111,
            "payment_type": constants.PAYMENT_TYPE_WALLET,
            "amount": 100000,
            "device": 1,
            "order_time": datetime.now(),
            "pay_time": datetime.now(),
            "finish_time": (datetime.now() + timedelta(days=1))
        }

    def test_course_order_comment(self):
        # 为普通用户test_user_1创建用户信息，用于购买课程
        UserProfile.objects.create(**self.user_profile_data)

        # 为拳手用户test_user_2创建1条订单数据(依次创建user_profile->boxer->club->course->course_order）
        self.user_profile_data['user'] = self.test_user_2
        UserProfile.objects.create(**self.user_profile_data)
        self.boxer_data['user'] = self.test_user_2
        boxer = BoxerIdentification.objects.create(**self.boxer_data)
        club = BoxingClub.objects.create(**self.club_data)
        self.course_data['club'] = club
        self.course_data['boxer'] = boxer
        course = Course.objects.create(**self.course_data)
        self.course_order_data['content_object'] = course
        course_order = PayOrder.objects.create(**self.course_order_data)

        # 获取订单的评论列表
        comment_list_res = self.client1.get(f'/course/order/{course_order.pk}/comment')
        self.assertEqual(len(comment_list_res.data['results']), 0)

        # 进行评论,并比对数据
        conmment_data = {
            "score": 6,
            "content": "i have comment",
            "images": ["img1.png", "img2.png", "img3.png"],
            "order": course_order.pk,
        }
        # 订单状态是待使用，不能进行评论
        do_comment_res = self.client1.post(f'/course/order/{course_order.pk}/comment', data=json.dumps(conmment_data), content_type='application/json')
        self.assertEqual(do_comment_res.status_code, status.HTTP_400_BAD_REQUEST)

        # 修改订单状态为待评论，可以正常评论
        course_order.status = constants.PAYMENT_STATUS_WAIT_COMMENT
        course_order.save()
        do_comment_res = self.client1.post(f'/course/order/{course_order.pk}/comment', data=json.dumps(conmment_data), content_type='application/json')
        self.assertEqual(do_comment_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(do_comment_res.data['user'], self.test_user_1.id)
        for key in conmment_data:
            self.assertEqual(do_comment_res.data[key], conmment_data[key])

        # 再次获取订单评论列表
        comment_list_res = self.client1.get(f'/course/order/{course_order.pk}/comment')
        self.assertEqual(len(comment_list_res.data['results']), 1)
