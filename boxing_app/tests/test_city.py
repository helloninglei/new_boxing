from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, BoxerIdentification, BoxingClub, Course


class CityTestCase(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(mobile='11111111111', password='password')
        self.test_user_2 = User.objects.create_user(mobile='11111111112', password='password')
        self.test_user_3 = User.objects.create_user(mobile='11111111113', password='password')
        self.test_user_4 = User.objects.create_user(mobile='11111111114', password='password')
        self.client1 = self.client_class()
        self.client2 = self.client_class()
        self.client3 = self.client_class()
        self.client4 = self.client_class()
        self.client1.login(username=self.test_user_1, password='password')
        self.client2.login(username=self.test_user_2, password='password')
        self.client3.login(username=self.test_user_3, password='password')
        self.client4.login(username=self.test_user_4, password='password')
        self.boxer_data = {
            "user": self.test_user_1,
            "real_name": "张三",
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "131313141444141444",
            "mobile": "11313131344",
            "is_professional_boxer": True,
            "club": "club1",
            "job": 'hhh',
            "introduction": "beautiful",
            "experience": '',
            "honor_certificate_images": ['http://img1.com', 'http://img2.com', 'http://img3.com'],
            "competition_video": 'https://baidu.com',
            "allowed_course": [constants.BOXER_ALLOWED_COURSES_BOXING, constants.BOXER_ALLOWED_COURSES_MMA,
                               constants.BOXER_ALLOWED_COURSES_THAI_BOXING],
            "is_accept_order": True
        }
        self.club_data = {
            "name": "club01",
            "address": "丰台区角门东洋桥",
            "longitude": 111.123456,
            "latitude": 11.123456,
            "city": "北京市",
            "city_index_letter": 'B',
            "phone": "11111111111",
            "opening_hours": "10:00--20:00",
            "images": ["www.baidu.com", "www.sina.com.cn"],
            "introduction": "最牛逼的拳馆"
        }
        self.course_data = {
            'boxer': None,
            'course_name': 'BOXING',
            'price': 1234,
            'duration': 120,
            'validity': "2018-01-11",
            'is_open': True,
            'price': 120,
            'duration': 365,
            'club': None
        }

    def test_boxer_city(self):
        boxer1 = BoxerIdentification.objects.create(**self.boxer_data)
        self.boxer_data['user'] = self.test_user_2
        boxer2 = BoxerIdentification.objects.create(**self.boxer_data)
        self.boxer_data['user'] = self.test_user_3
        boxer3 = BoxerIdentification.objects.create(**self.boxer_data)
        self.boxer_data['user'] = self.test_user_4
        boxer4 = BoxerIdentification.objects.create(**self.boxer_data)

        club1 = BoxingClub.objects.create(**self.club_data)
        self.club_data['name'] = 'club2'
        self.club_data['city'] = '广州市'
        self.club_data['city_index_letter'] = 'G'
        club2 = BoxingClub.objects.create(**self.club_data)
        self.club_data['name'] = 'club3'
        self.club_data['city'] = '长春市'
        self.club_data['city_index_letter'] = 'C'
        club3 = BoxingClub.objects.create(**self.club_data)
        self.club_data['name'] = 'club4'
        self.club_data['city'] = '重庆市'
        self.club_data['city_index_letter'] = 'C'
        club4 = BoxingClub.objects.create(**self.club_data)

        self.course_data['boxer'] = boxer1
        self.course_data['club'] = club1
        Course.objects.create(**self.course_data)
        self.course_data['boxer'] = boxer2
        self.course_data['club'] = club2
        Course.objects.create(**self.course_data)
        self.course_data['boxer'] = boxer3
        self.course_data['club'] = club3
        Course.objects.create(**self.course_data)
        self.course_data['boxer'] = boxer4
        self.course_data['club'] = club4
        Course.objects.create(**self.course_data)

        res = self.client1.get('/boxer_cities')
        self.assertEqual(len(res.data['boxerCityList']), 4)
        self.assertEqual(res.data['boxerCityList'][0], {'cityLetter': 'B', 'cityName': '北京市'})
        self.assertEqual(res.data['boxerCityList'][1]['cityLetter'], 'C')
        self.assertEqual(res.data['boxerCityList'][2]['cityLetter'], 'C')
        self.assertEqual(res.data['boxerCityList'][3], {'cityLetter': 'G', 'cityName': '广州市'})
