from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, BoxerIdentification, Course, BoxingClub, UserProfile, PayOrder, OrderComment


class CommentsAboutBoxerTestCase(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(mobile='11111111111', password='password')
        self.test_user_2 = User.objects.create_user(mobile='11111111112', password='password')
        self.test_user_3 = User.objects.create_user(mobile='11111111113', password='password')
        self.client1 = self.client_class(HTTP_SOURCE='iOS')
        self.client2 = self.client_class(HTTP_SOURCE='iOS')
        self.client3 = self.client_class(HTTP_SOURCE='iOS')
        self.client1.login(username=self.test_user_1, password='password')
        self.client2.login(username=self.test_user_2, password='password')
        self.client3.login(username=self.test_user_3, password='password')
        self.user_profile_data = {
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
        self.conmment_data = {
            "score": 6,
            "content": "i have comment",
            "images": ["img1.png", "img2.png", "img3.png"],
            "order": None,
            "user": self.test_user_1
        }

    def test_get_boxer_comments(self):
        # 为普通用户test_user_1创建用户信息，用于购买课程
        for user in [self.test_user_1, self.test_user_2, self.test_user_3]:
            UserProfile.objects.filter(user=user).update(**self.user_profile_data)

        # 为拳手用户test_user_2创建2条订单数据(依次创建user_profile->boxer->club->course->course_order）
        self.boxer_data['user'] = self.test_user_2
        boxer = BoxerIdentification.objects.create(**self.boxer_data)
        club = BoxingClub.objects.create(**self.club_data)
        self.course_data['club'] = club
        self.course_data['boxer'] = boxer
        course = Course.objects.create(**self.course_data)
        self.course_order_data['content_object'] = course
        PayOrder.objects.create(**self.course_order_data)
        PayOrder.objects.create(**self.course_order_data)

        # 为拳手用户test_user_3创建3条订单数据
        self.boxer_data['user'] = self.test_user_3
        boxer = BoxerIdentification.objects.create(**self.boxer_data)
        self.club_data['name'] = 'club02'
        club = BoxingClub.objects.create(**self.club_data)
        self.course_data['club'] = club
        self.course_data['boxer'] = boxer
        course = Course.objects.create(**self.course_data)
        self.course_order_data['content_object'] = course
        order1 = PayOrder.objects.create(**self.course_order_data)
        order2 = PayOrder.objects.create(**self.course_order_data)
        PayOrder.objects.create(**self.course_order_data)

        # 对拳手test_user_3的订单order1、order2创建2条评论
        self.conmment_data['order'] = order1
        OrderComment.objects.create(**self.conmment_data)
        self.conmment_data['score'] = 5
        self.conmment_data['order'] = order2
        OrderComment.objects.create(**self.conmment_data)

        # 获取拳手评论列表
        res = self.client3.get(f'/boxer/{boxer.id}/comments')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)
        self.assertEqual(res.data['count'], 2)
        self.assertEqual(res.data['avg_score'], (6+5)/2)
        for key in self.conmment_data:
            # user为购买者
            if key == 'user':
                self.assertEqual(res.data['results'][0][key]['id'], self.test_user_1.id)
                self.assertEqual(res.data['results'][0][key]['nick_name'], self.user_profile_data['nick_name'])
                self.assertEqual(res.data['results'][0][key]['avatar'], self.user_profile_data['avatar'])
            elif key == 'order':
                self.assertEqual(res.data['results'][0][key], order2.id)
            else:
                self.assertEqual(res.data['results'][0][key], self.conmment_data[key])
