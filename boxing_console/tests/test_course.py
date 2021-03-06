from datetime import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, BoxerIdentification, Course, BoxingClub


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(mobile='11111111111', password='password')
        self.client = self.client_class()
        self.client.login(username=self.user1, password='password')

    @staticmethod
    def make_identification_list():
        user_list = [User.objects.create_superuser(mobile=str(11111111112+num), password='password')
                     for num in range(0, 10)]

        identification_list = [BoxerIdentification.objects.create(
            user=user,
            real_name='name{}'.format(user.pk),
            height=100 + int(user.pk),
            weight=60 + int(user.pk),
            birthday=datetime.now(),
            identity_number=100000000000000000 + int(user.pk),
            mobile=str(13000000000 + int(user.id)),
            job='job{}'.format(user.id),
            introduction='introduction{}'.format(user.id),
            honor_certificate_images=['http://img{}.com'.format(user.id)],
            competition_video='https://baidu{}.com'.format(user.id))
            for user in user_list]
        return identification_list

    def test_courses_list(self):
        identification_list = self.make_identification_list()
        identification_list[1].is_locked = True
        identification_list[2].is_locked = True
        identification_list[3].is_locked = True
        identification_list[4].is_locked = False
        identification_list[1].real_name = "张三"
        identification_list[2].real_name = "李四"
        identification_list[3].real_name = "王五"
        identification_list[4].real_name = "王八"
        identification_list[1].save()
        identification_list[2].save()
        identification_list[3].save()
        identification_list[4].save()

        club_data = {
            "name": "club01",
            "address": "club_address",
            "longitude": 111.111111,
            "latitude": 11.111111,
            "phone": 11111111111,
            "opening_hours": "9:00-22:00",
            "images": ["www.baidu.png"],
            "introduction": "club_introduction"
        }
        club = BoxingClub.objects.create(**club_data)

        data1 = {"boxer": identification_list[1],
                 "course_name": constants.BOXER_ALLOWED_COURSES_MMA,
                 "price": 100,
                 "duration": 120,
                 "validity": "2018-08-25",
                 "club": club
                 }

        data2 = {"boxer": identification_list[2],
                 "course_name": constants.BOXER_ALLOWED_COURSES_BOXING,
                 "price": 120,
                 "duration": 120,
                 "validity": "2018-08-25",
                 "club": club
                 }

        data3 = {"boxer": identification_list[3],
                 "course_name": constants.BOXER_ALLOWED_COURSES_FREE_BOXING,
                 "price": 130,
                 "duration": 120,
                 "validity": "2018-08-25",
                 "club": club
                 }

        data4 = {"boxer": identification_list[4],
                 "course_name": constants.BOXER_ALLOWED_COURSES_BOXING,
                 "price": 140,
                 "duration": 120,
                 "validity": "2018-08-25",
                 "club": club
                 }

        Course.objects.create(**data1)
        Course.objects.create(**data2)
        Course.objects.create(**data3)
        Course.objects.create(**data4)

        res = self.client.get(reverse('courses_list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 4)

        # 通过course_name过滤
        res = self.client.get('/courses?course_name={}'.format(data1['course_name']))
        self.assertEqual(res.data['count'], 1)
        # 检查数据是否完整
        for key in data1:
            if key == 'boxer':
                self.assertEqual(res.data['results'][0]['boxer_name'], data1[key].real_name)
            elif key == 'club':
                self.assertEqual(res.data['results'][0][key], data1[key].pk)
            else:
                self.assertEqual(res.data['results'][0][key], data1[key])

        # 通过is_accept_order过滤,注意，is_accept_order与拳手的is_locked是相反的
        res = self.client.get('/courses?is_accept_order={}'.format(True))
        self.assertEqual(res.data['count'], 1)

        # 通过price_min过滤
        res = self.client.get('/courses?price_min={}'.format(data3['price']))
        self.assertEqual(res.data['count'], 2)

        # 通过price_max过滤
        res = self.client.get('/courses?price_max={}'.format(data3['price']))
        self.assertEqual(res.data['count'], 3)

        # 通过boxer__real_name搜索
        res = self.client.get('/courses?search={}'.format(identification_list[3].real_name))
        self.assertEqual(res.data['count'], 1)

        # 通过boxer__mobile搜索
        res = self.client.get('/courses?search={}'.format(identification_list[1].user.mobile))
        self.assertEqual(res.data['count'], 1)

    def test_get_course_detail(self):
        identification_list = self.make_identification_list()

        # 创建拳馆，用于创建课程
        club_data = {
            "name": "club01",
            "address": "club_address",
            "longitude": 111.111111,
            "latitude": 11.111111,
            "phone": 11111111111,
            "opening_hours": "9:00-22:00",
            "images": ["www.baidu.png"],
            "introduction": "club_introduction"
        }
        club = BoxingClub.objects.create(**club_data)

        # 拳手的信息
        update_data = {"real_name": "老王",
                       "mobile": '10000000000',
                       "allowed_course": [constants.BOXER_ALLOWED_COURSES_FREE_BOXING,
                                          constants.BOXER_ALLOWED_COURSES_BOXING,
                                          constants.BOXER_ALLOWED_COURSES_MMA],
                       "is_professional_boxer": True
                       }
        [setattr(identification_list[1], key, update_data[key]) for key in update_data]
        identification_list[1].save()

        # 创建课程
        data = {"boxer": identification_list[1],
                "course_name": constants.BOXER_ALLOWED_COURSES_MMA,
                "price": 100,
                "duration": 120,
                "validity": "2018-08-25",
                "club": club
                }
        course = Course.objects.create(**data)

        res = self.client.get(reverse('course_detail', kwargs={'pk': course.pk}))

        # 比较课程详情中不属于拳手部分的信息
        for key in data:
            if key == 'boxer':
                self.assertEqual(res.data['boxer_name'], data[key].real_name)
            elif key == 'club':
                self.assertEqual(res.data[key], data[key].pk)
            else:
                self.assertEqual(res.data[key], data[key])

        # 比较课程详情中属于拳手部分的信息
        for key in update_data:
            if key == 'real_name':
                self.assertEqual(res.data['boxer_name'], update_data[key])
            elif key == 'mobile':
                self.assertEqual(res.data[key], data['boxer'].user.mobile)
            else:
                self.assertEqual(res.data[key], update_data[key])
        self.assertIsNot(res.data['is_accept_order'], data['boxer'].is_locked)

