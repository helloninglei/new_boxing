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

    def test_get_boxer_order_list(self):

        # 为普通用户test_user_1创建用户信息，用于购买课程
        UserProfile.objects.create(**self.user_profile_data)

        # 为拳手用户test_user_2创建2条订单数据(依次创建user_profile->boxer->club->course->course_order）
        self.user_profile_data['user'] = self.test_user_2
        UserProfile.objects.create(**self.user_profile_data)
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
        self.user_profile_data['user'] = self.test_user_3
        UserProfile.objects.create(**self.user_profile_data)
        self.boxer_data['user'] = self.test_user_3
        boxer = BoxerIdentification.objects.create(**self.boxer_data)
        self.club_data['name'] = 'club02'
        club = BoxingClub.objects.create(**self.club_data)
        self.course_data['club'] = club
        self.course_data['boxer'] = boxer
        course = Course.objects.create(**self.course_data)
        self.course_order_data['content_object'] = course
        PayOrder.objects.create(**self.course_order_data)
        PayOrder.objects.create(**self.course_order_data)
        PayOrder.objects.create(**self.course_order_data)

        res = self.client2.get('/boxer/orders')
        self.assertEqual(len(res.data['results']), 2)

        res = self.client3.get('/boxer/orders')
        self.assertEqual(len(res.data['results']), 3)

    def test_get_boxer_order_detail(self):
        # 为普通用户test_user_1创建用户信息，用于购买课程
        UserProfile.objects.create(**self.user_profile_data)

        # 为拳手用户test_user_4创建1条订单数据(依次创建user_profile->boxer->club->course->course_order）
        self.user_profile_data['user'] = self.test_user_4
        UserProfile.objects.create(**self.user_profile_data)
        self.boxer_data['user'] = self.test_user_4
        boxer = BoxerIdentification.objects.create(**self.boxer_data)
        club = BoxingClub.objects.create(**self.club_data)
        self.course_data['club'] = club
        self.course_data['boxer'] = boxer
        course = Course.objects.create(**self.course_data)
        self.course_order_data['content_object'] = course
        courser_order = PayOrder.objects.create(**self.course_order_data)

        res = self.client4.get(f'/boxer/order/{courser_order.pk}')
        self.assertEqual(res.data['status'], self.course_order_data['status'])
        self.assertEqual(res.data['out_trade_no'], self.course_order_data['out_trade_no'])
        self.assertEqual(res.data['payment_type'], self.course_order_data['payment_type'])
        self.assertEqual(res.data['amount'], self.course_order_data['amount'])
        self.assertEqual(res.data['order_time'], self.course_order_data['order_time'].strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(res.data['pay_time'], self.course_order_data['pay_time'].strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(res.data['finish_time'], self.course_order_data['finish_time'].strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(res.data['user_id'], self.test_user_1.id)
        self.assertEqual(res.data['user_nickname'],  self.user_profile_data['nick_name'])
        self.assertEqual(res.data['user_gender'],  self.user_profile_data['gender'])
        self.assertEqual(res.data['user_avatar'],  self.user_profile_data['avatar'])
        self.assertEqual(res.data['course_name'], self.course_data['course_name'])
        self.assertEqual(res.data['course_duration'], self.course_data['duration'])
        self.assertEqual(res.data['course_validity'].strftime('%Y-%m-%d'), self.course_data['validity'])
        self.assertEqual(res.data['club_name'], self.club_data['name'])
        self.assertEqual(res.data['club_address'], self.club_data['address'])
        self.assertEqual(str(res.data['club_longitude']), str(self.club_data['longitude']))
        self.assertEqual(str(res.data['club_latitude']), str(self.club_data['latitude']))
        # TODO 缺少订单评论

    def test_get_user_order_list(self):
        # 分别为test_user_1、2、3、4创建user_profile
        self.user_profile_data['user'] = self.test_user_1
        UserProfile.objects.create(**self.user_profile_data)
        self.user_profile_data['user'] = self.test_user_2
        UserProfile.objects.create(**self.user_profile_data)
        self.user_profile_data['user'] = self.test_user_3
        UserProfile.objects.create(**self.user_profile_data)
        self.user_profile_data['user'] = self.test_user_4
        UserProfile.objects.create(**self.user_profile_data)

        # 为拳手用户test_user_1创建1个课程(依次创建user_profile->boxer->club->course）
        self.boxer_data['user'] = self.test_user_4
        boxer = BoxerIdentification.objects.create(**self.boxer_data)
        club = BoxingClub.objects.create(**self.club_data)
        self.course_data['club'] = club
        self.course_data['boxer'] = boxer
        course = Course.objects.create(**self.course_data)
        self.course_order_data['content_object'] = course

        # 用户test_user_2购买课程2个课程
        self.course_order_data['user'] = self.test_user_2
        PayOrder.objects.create(**self.course_order_data)
        PayOrder.objects.create(**self.course_order_data)

        # 用户test_user_3购买课程3个课程
        self.course_order_data['user'] = self.test_user_3
        PayOrder.objects.create(**self.course_order_data)
        PayOrder.objects.create(**self.course_order_data)
        PayOrder.objects.create(**self.course_order_data)

        # 用户test_user_2获取订单列表,结果应为2条
        res = self.client2.get('/user/orders')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

        # 用户test_user_3获取订单列表，结果应为3条
        res = self.client3.get('/user/orders')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 3)

        # 用户test_user_4获取订单列表，结果应为0条
        res = self.client4.get('/user/orders')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 0)

    def test_get_user_order_detail(self):
        # 为拳手用户test_user_1创建1个课程(依次创建user_profile->boxer->club->course）
        self.user_profile_data['user'] = self.test_user_1
        UserProfile.objects.create(**self.user_profile_data)
        self.boxer_data['user'] = self.test_user_1
        boxer = BoxerIdentification.objects.create(**self.boxer_data)
        club = BoxingClub.objects.create(**self.club_data)
        self.course_data['club'] = club
        self.course_data['boxer'] = boxer
        course = Course.objects.create(**self.course_data)

        # 为普通用户test_user_2创建用户信息，并购买课程
        self.user_profile_data['user'] = self.test_user_2
        self.course_order_data['content_object'] = course
        self.course_order_data['user'] = self.test_user_2
        course_order = PayOrder.objects.create(**self.course_order_data)

        # 用户test_user_2获取所购买课程的详情
        res = self.client2.get(f'/user/order/{course_order.pk}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], self.course_order_data['status'])
        self.assertEqual(res.data['out_trade_no'], self.course_order_data['out_trade_no'])
        self.assertEqual(res.data['payment_type'], self.course_order_data['payment_type'])
        self.assertEqual(res.data['amount'], self.course_order_data['amount'])
        self.assertEqual(res.data['order_time'], self.course_order_data['order_time'].strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(res.data['pay_time'], self.course_order_data['pay_time'].strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(res.data['finish_time'], self.course_order_data['finish_time'].strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(res.data['boxer_id'], boxer.id)
        self.assertEqual(res.data['boxer_name'], boxer.real_name)
        self.assertEqual(res.data['boxer_gender'], boxer.user.user_profile.gender)
        self.assertEqual(res.data['boxer_avatar'], boxer.user.user_profile.avatar)
        self.assertEqual(res.data['course_name'], self.course_data['course_name'])
        self.assertEqual(res.data['course_duration'], self.course_data['duration'])
        self.assertEqual(res.data['course_validity'].strftime('%Y-%m-%d'), self.course_data['validity'])
        self.assertEqual(res.data['club_name'], self.club_data['name'])
        self.assertEqual(res.data['club_address'], self.club_data['address'])
        self.assertEqual(str(res.data['club_longitude']), str(self.club_data['longitude']))
        self.assertEqual(str(res.data['club_latitude']), str(self.club_data['latitude']))