from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from biz import constants
from biz.models import User, BoxerIdentification, Course, BoxingClub


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(mobile='11111111111', password='password')
        self.user2 = User.objects.create_user(mobile='11111111112', password='password')
        self.client1 = self.client_class()
        self.client2 = self.client_class()
        self.client1.login(username=self.user1, password='password')
        self.client2.login(username=self.user2, password='password')
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
                    "competition_video": 'https://baidu.com',
                    "allowed_course": [constants.BOXER_ALLOWED_COURSES_BOXING, constants.BOXER_ALLOWED_COURSES_MMA]
                }
        self.club_data = {
                    "name": "club01",
                    "address": "丰台区角门东洋桥",
                    "longitude": 111.123456,
                    "latitude": 11.123456,
                    "phone": "11111111111",
                    "opening_hours": "10:00--20:00",
                    "images": ["www.baidu.com", "www.sina.com.cn"],
                    "introduction": "最牛逼的拳馆"
                    }

    def test_update_boxer_course(self):
        # 创建拳手，并根据拳手allowed_course为拳手创建课程
        identification = BoxerIdentification.objects.create(**self.boxer_data)
        for course_name in self.boxer_data['allowed_course']:
            Course.objects.create(boxer=identification, course_name=course_name)
        # 获取拳手课程初始列表，判断列表数量是否与拳手可开课程数量一致
        course_list_res = self.client1.get('/boxer/course')
        self.assertEqual(len(course_list_res.data['results']), len(self.boxer_data['allowed_course']))

        # 构造修改课程列表数据，并修改课程
        my_club = BoxingClub.objects.create(**self.club_data)
        course1_data = {
            'course_id': course_list_res.data['results'][0].get('id'),
            'price': 120,
            'duration': 365,
        }
        course2_data = {
            'course_id': course_list_res.data['results'][1].get('id'),
            'price': 120,
            'duration': 366,
        }
        update_course_data = {
            "validity": "2018-04-25",
            "club": my_club.pk,
            "course_list": [{**course1_data}, {**course2_data}]}
        update_res = self.client1.post('/boxer/course', data=json.dumps(update_course_data),
                                       content_type='application/json')
        self.assertEqual(update_res.status_code, status.HTTP_200_OK)

        # 获取修改后的课程数据,
        course_list_res = self.client1.get('/boxer/course')
        course_result = course_list_res.data['results']
        self.assertEqual(len(course_list_res.data['results']), len(self.boxer_data['allowed_course']))
        self.assertEqual(course_result[0]['id'], course1_data['course_id'])
        self.assertEqual(course_result[0]['price'], course1_data['price'])
        self.assertEqual(course_result[0]['duration'], course1_data['duration'])
        self.assertEqual(course_result[0]['validity'], update_course_data['validity'])
        self.assertEqual(course_result[0]['club'], update_course_data['club'])
        self.assertEqual(course_result[0]['validity'], update_course_data['validity'])
        self.assertEqual(course_result[0]['club_name'], self.club_data['name'])
        self.assertEqual(course_result[0]['club_address'], self.club_data['address'])
        self.assertEqual(str(course_result[0]['club_longitude']), str(self.club_data['longitude']))
        self.assertEqual(str(course_result[0]['club_latitude']), str(self.club_data['latitude']))
