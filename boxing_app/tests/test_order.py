from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, UserProfile, BoxerIdentification, BoxingClub, Course, PayOrder, OrderComment, CourseOrder


class OrderTestCase(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(mobile='11111111111', password='password')
        self.test_user_2 = User.objects.create_user(mobile='11111111112', password='password')
        self.test_user_3 = User.objects.create_user(mobile='11111111113', password='password')
        self.test_user_4 = User.objects.create_user(mobile='11111111114', password='password')
        self.test_user = None
        self.client1 = self.client_class(HTTP_SOURCE='iOS')
        self.client2 = self.client_class(HTTP_SOURCE='iOS')
        self.client3 = self.client_class(HTTP_SOURCE='iOS')
        self.client4 = self.client_class(HTTP_SOURCE='iOS')
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
        self.comment_data = {
            "score": 6,
            "content": "i have comment",
            "images": ["img1.png", "img2.png", "img3.png"],
            "order": None,
            "user": self.test_user_1
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
        self.client1.post('/user/orders', data={'id': course.id})
        self.client1.post('/user/orders', data={'id': course.id})

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
        self.client1.post('/user/orders', data={'id': course.id})
        CourseOrder.objects.filter(course=course).update(status=constants.PAYMENT_STATUS_FINISHED)
        self.client1.post('/user/orders', data={'id': course.id})
        self.client1.post('/user/orders', data={'id': course.id})

        # 拳手2获取2条订单数据
        res = self.client2.get('/boxer/orders')
        self.assertEqual(len(res.data['results']), 2)
        # 拳手3获取3条订单数据
        res = self.client3.get('/boxer/orders')
        self.assertEqual(len(res.data['results']), 3)

        # 通过状态过滤
        res = self.client3.get('/boxer/orders', {'status': constants.PAYMENT_STATUS_UNPAID})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)
        res = self.client3.get('/boxer/orders', {'status': constants.PAYMENT_STATUS_WAIT_USE})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 0)
        res = self.client3.get('/boxer/orders', {'status': constants.PAYMENT_STATUS_FINISHED})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)

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
        # 不能购买自己的课程
        res = self.client4.post('/user/orders', data={'id': course.id})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.client1.post('/user/orders', data={'id': course.id})
        # 为订单创建评论
        course_order = CourseOrder.objects.get(course=course)
        self.comment_data['order'] = course_order
        OrderComment.objects.create(**self.comment_data)

        res = self.client4.get(f'/boxer/order/{course_order.pk}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], constants.PAYMENT_STATUS_UNPAID)
        self.assertEqual(res.data['user_id'], self.test_user_1.id)
        self.assertEqual(res.data['user_nickname'],  self.user_profile_data['nick_name'])
        self.assertEqual(res.data['user_gender'],  self.user_profile_data['gender'])
        self.assertEqual(res.data['user_avatar'],  self.user_profile_data['avatar'])
        self.assertEqual(res.data['course_name'], self.course_data['course_name'])
        self.assertEqual(res.data['course_duration'], self.course_data['duration'])
        self.assertEqual(res.data['course_validity'], self.course_data['validity'])
        self.assertEqual(res.data['club_id'], club.id)
        self.assertEqual(res.data['club_name'], self.club_data['name'])
        self.assertEqual(res.data['club_address'], self.club_data['address'])
        self.assertEqual(str(res.data['club_longitude']), str(self.club_data['longitude']))
        self.assertEqual(str(res.data['club_latitude']), str(self.club_data['latitude']))
        self.assertEqual(res.data['comment_score'], self.comment_data['score'])
        self.assertEqual(res.data['comment_images'], self.comment_data['images'])
        self.assertEqual(res.data['comment_score'], self.comment_data['score'])
        self.assertIsNotNone(res.data['comment_time'])

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

        # 用户test_user_2购买课程2个课程
        self.client2.post('/user/orders', data={'id': course.id})
        self.client2.post('/user/orders', data={'id': course.id})

        # 用户test_user_3购买课程3个课程
        self.client3.post('/user/orders', data={'id': course.id})
        CourseOrder.objects.filter(course=course).update(status=constants.PAYMENT_STATUS_FINISHED)
        self.client3.post('/user/orders', data={'id': course.id})
        self.client3.post('/user/orders', data={'id': course.id})

        # 用户test_user_2获取订单列表,结果应为2条
        res = self.client2.get('/user/orders')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

        # 用户test_user_3获取订单列表，结果应为3条
        res = self.client3.get('/user/orders')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 3)
        # 通过状态过滤
        res = self.client3.get('/user/orders', {'status': constants.PAYMENT_STATUS_UNPAID})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)
        res = self.client3.get('/user/orders', {'status': constants.PAYMENT_STATUS_WAIT_USE})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 0)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client3.get('/user/orders', {'status': constants.PAYMENT_STATUS_FINISHED})
        self.assertEqual(len(res.data['results']), 1)

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
        self.client2.post('/user/orders', data={'id': course.id})
        course_order = CourseOrder.objects.get(course=course)
        # 用户test_user_2获取所购买课程的详情
        res = self.client2.get(f'/user/order/{course_order.id}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], constants.PAYMENT_STATUS_UNPAID)
        self.assertEqual(res.data['boxer_id'], boxer.id)
        self.assertEqual(res.data['boxer_name'], boxer.real_name)
        self.assertEqual(res.data['boxer_gender'], boxer.user.user_profile.gender)
        self.assertEqual(res.data['boxer_avatar'], boxer.user.user_profile.avatar)
        self.assertEqual(res.data['course_name'], self.course_data['course_name'])
        self.assertEqual(res.data['course_duration'], self.course_data['duration'])
        self.assertEqual(res.data['course_validity'], self.course_data['validity'])
        self.assertEqual(res.data['club_id'], club.id)
        self.assertEqual(res.data['club_name'], self.club_data['name'])
        self.assertEqual(res.data['club_address'], self.club_data['address'])
        self.assertEqual(str(res.data['club_longitude']), str(self.club_data['longitude']))
        self.assertEqual(str(res.data['club_latitude']), str(self.club_data['latitude']))

    def test_create_course_order(self):
        # 为拳手用户test_user_1创建1个课程
        self.user_profile_data['user'] = self.test_user_1
        UserProfile.objects.create(**self.user_profile_data)
        self.boxer_data['user'] = self.test_user_1
        boxer = BoxerIdentification.objects.create(**self.boxer_data)
        club = BoxingClub.objects.create(**self.club_data)
        self.course_data['club'] = club
        self.course_data['boxer'] = boxer
        course = Course.objects.create(**self.course_data)

        # test_user_2成功创建了未支付订单
        res = self.client2.post('/user/orders', data={'id': course.id})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # 查询课程的订单，核对支付订单数据
        self.assertEqual(course.course_orders.count(), 1)
        course_order = CourseOrder.objects.get(course=course)
        self.assertIsNone(course_order.pay_order)
        self.assertEqual(course_order.boxer, boxer)
        self.assertEqual(course_order.course, course)

    def test_delete_order(self):
        # 为拳手用户test_user_1创建1个课程
        self.user_profile_data['user'] = self.test_user_1
        UserProfile.objects.create(**self.user_profile_data)
        self.boxer_data['user'] = self.test_user_1
        boxer = BoxerIdentification.objects.create(**self.boxer_data)
        club = BoxingClub.objects.create(**self.club_data)
        self.course_data['club'] = club
        self.course_data['boxer'] = boxer
        course = Course.objects.create(**self.course_data)

        # test_user_2创建未支付订单
        self.client2.post('/user/orders', data={'id': course.id})
        course_order = CourseOrder.objects.get(course=course)
        # 不能删除不是未支付状态的支付订单
        CourseOrder.objects.filter(user=self.test_user_2).update(status=constants.PAYMENT_STATUS_WAIT_COMMENT)
        res = self.client2.delete(f'/user/order/{course_order.id}')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'], '订单不是未支付状态，不能删除')
        # 可以删除未支付状态的支付订单
        CourseOrder.objects.filter(user=self.test_user_2).update(status=constants.PAYMENT_STATUS_UNPAID)
        res = self.client2.delete(f'/user/order/{course_order.id}')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CourseOrder.objects.filter(id=course_order.id).exists())
