from datetime import datetime

from rest_framework.test import APITestCase

from biz import constants, redis_client
from biz.constants import USER_TYPE_MAP, USER_TYPE_BOXER
from biz.models import User, BoxerIdentification, Course, BoxingClub, UserProfile, CourseOrder
from biz.services.url_service import get_cdn_url


class NearbyBoxerTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(mobile='11111111111', password='password')
        self.user2 = User.objects.create_user(mobile='11111111112', password='password')
        self.user3 = User.objects.create_user(mobile='11111111113', password='password')
        self.user4 = User.objects.create_user(mobile='11111111114', password='password')
        self.user5 = User.objects.create_user(mobile='11111111115', password='password')
        self.user6 = User.objects.create_user(mobile='11111111116', password='password')
        self.client1 = self.client_class()
        self.client2 = self.client_class()
        self.client3 = self.client_class()
        self.client4 = self.client_class()
        self.client5 = self.client_class()
        self.client6 = self.client_class()
        self.client1.login(username=self.user1, password='password')
        self.client2.login(username=self.user2, password='password')
        self.client3.login(username=self.user3, password='password')
        self.client4.login(username=self.user4, password='password')
        self.client5.login(username=self.user5, password='password')
        self.client6.login(username=self.user6, password='password')
        redis_client.redis_client.flushdb()
        self.user_profile_data = {
            "nick_name": "nike_name",
            "gender": True,
            "name": "name",
            "nation": "nation",
            "avatar": "avatar"
        }
        self.boxer_data = {
            "user": self.user1,
            "real_name": "boxer name",
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "131313141444141444",
            "mobile": "11313131344",
            "is_professional_boxer": True,
            "club": "club1",
            "job": 'teacher',
            "introduction": "boxer introduction",
            "experience": 'boxer experience',
            "authentication_state": constants.BOXER_AUTHENTICATION_STATE_APPROVED,
            "honor_certificate_images": ['http://img1.com', 'http://img2.com', 'http://img3.com'],
            "competition_video": 'https://baidu.com',
            "is_accept_order": True,
            "allowed_course": [constants.BOXER_ALLOWED_COURSES_BOXING, constants.BOXER_ALLOWED_COURSES_MMA,
                               constants.BOXER_ALLOWED_COURSES_FREE_BOXING]
        }
        self.club1_data = {
            "name": "??????????????????",
            "address": "????????????",
            "city": "?????????",
            "longitude": 116.318031,
            "latitude": 39.999222,
            "phone": "11111111111",
            "opening_hours": "10:00--20:00",
            "images": ["www.baidu.com", "www.sina.com.cn"],
            "introduction": "??????????????????"
        }
        self.club2_data = {
            "name": "??????????????????",
            "address": "????????????",
            "city": "?????????",
            "longitude": 116.332404,
            "latitude": 40.01116,
            "phone": "11111111111",
            "opening_hours": "10:00--20:00",
            "images": ["www.baidu.com", "www.sina.com.cn"],
            "introduction": "??????????????????"
        }
        self.club3_data = {
            "name": "???????????????????????????",
            "address": "????????????",
            "city": "?????????",
            "longitude": 116.453712,
            "latitude": 39.937732,
            "phone": "11111111111",
            "opening_hours": "10:00--20:00",
            "images": ["www.baidu.com", "www.sina.com.cn"],
            "introduction": "??????????????????"
        }
        self.club4_data = {
            "name": "???????????????",
            "address": "???????????????",
            "city": "?????????",
            "longitude": 114.496699,
            "latitude": 38.05242,
            "phone": "11111111111",
            "opening_hours": "10:00--20:00",
            "images": ["www.baidu.com", "www.sina.com.cn"],
            "introduction": "??????????????????"
        }
        self.club5_data = {
            "name": "????????????",
            "address": "?????????",
            "city": "?????????",
            "longitude": 106.657151,
            "latitude": 29.516309,
            "phone": "11111111111",
            "opening_hours": "10:00--20:00",
            "images": ["www.baidu.com", "www.sina.com.cn"],
            "introduction": "??????????????????"
        }
        self.course_data = {
            "club": None,
            "boxer": None,
            'is_open': True,
            'price': 122,
            'duration': 367,
            "validity": "2118-04-25",
            "course_name": constants.BOXER_ALLOWED_COURSES_BOXING
        }

    def test_get_nearby_boxer(self):
        # ??????club1-4
        club1 = BoxingClub.objects.create(**self.club1_data)
        club2 = BoxingClub.objects.create(**self.club2_data)
        club3 = BoxingClub.objects.create(**self.club3_data)
        club4 = BoxingClub.objects.create(**self.club4_data)

        # ???user1-5??????user_profile
        for user in [self.user1, self.user2, self.user3, self.user4, self.user5]:
            UserProfile.objects.filter(user=user).update(**self.user_profile_data)

        # ??????boxer1-5,
        self.boxer_data['user'] = self.user1
        self.boxer_data['real_name'] = 'boxer1'
        boxer1 = BoxerIdentification.objects.create(**self.boxer_data)
        self.boxer_data['user'] = self.user2
        self.boxer_data['real_name'] = 'boxer2'
        boxer2 = BoxerIdentification.objects.create(**self.boxer_data)
        self.boxer_data['user'] = self.user3
        self.boxer_data['real_name'] = 'boxer3'
        boxer3 = BoxerIdentification.objects.create(**self.boxer_data)
        self.boxer_data['user'] = self.user4
        self.boxer_data['real_name'] = 'boxer4'
        boxer4 = BoxerIdentification.objects.create(**self.boxer_data)
        self.boxer_data['user'] = self.user5
        self.boxer_data['real_name'] = 'boxer5'
        boxer5 = BoxerIdentification.objects.create(**self.boxer_data)
        User.objects.all().update(user_type=USER_TYPE_BOXER)

        # ?????????boxer1-5?????????????????????course5???course1???club??????
        self.course_data['club'] = club1
        self.course_data['boxer'] = boxer1
        Course.objects.create(**self.course_data)
        self.course_data['club'] = club2
        self.course_data['boxer'] = boxer2
        Course.objects.create(**self.course_data)
        self.course_data['club'] = club3
        self.course_data['boxer'] = boxer3
        Course.objects.create(**self.course_data)
        self.course_data['club'] = club4
        self.course_data['boxer'] = boxer4
        Course.objects.create(**self.course_data)
        self.course_data['club'] = club1
        self.course_data['boxer'] = boxer5
        course5 = Course.objects.create(**self.course_data)

        # ???boxer1-5???????????????redis(boxer????????????????????????club??????????????????boxer1???boxer5???????????????
        redis_client.record_object_location(boxer1, club1.longitude, club1.latitude)
        redis_client.record_object_location(boxer2, club2.longitude, club2.latitude)
        redis_client.record_object_location(boxer3, club3.longitude, club3.latitude)
        redis_client.record_object_location(boxer4, club4.longitude, club4.latitude)
        redis_client.record_object_location(boxer5, club1.longitude, club1.latitude)

        # ????????????????????????????????????????????????????????????????????????????????????????????????116.39737,40.024919)
        res = self.client6.get(f'/nearby/boxers', {'longitude': 116.39737, 'latitude': 40.024919})
        # ????????????boxer????????????????????????redis??????????????????????????????
        boxer_list = redis_client.get_near_object(BoxerIdentification, 116.39737, 40.024919)
        boxer_id_list = [item[0] for item in boxer_list]
        nearby_boxer_id_list = [str(res.data['results'][i]['id']) for i in range(len(res.data['results']))]
        self.assertEqual(boxer_id_list, nearby_boxer_id_list)

        # ???boxer5???????????????????????????,??????????????????(????????????????????????boxer5????????????boxer1???????????????
        self.client1.post('/course/order', data={'id': course5.id})
        CourseOrder.objects.filter(course=course5.id, user=self.user1).update(
            status=constants.COURSE_PAYMENT_STATUS_FINISHED, pay_time=datetime.now())
        for index, boxer_id in enumerate(boxer_id_list):
            if int(boxer_id) == boxer1.id:
                boxer1_index = index
            elif int(boxer_id) == boxer5.id:
                boxer5_index = index
        if boxer5_index > boxer1_index:
            boxer_id_list[boxer5_index], boxer_id_list[boxer1_index] = str(boxer1.id), str(boxer5.id)
        res = self.client6.get('/nearby/boxers', data={'longitude': 116.39737, 'latitude': 40.024919})
        nearby_boxer_id_list = [str(res.data['results'][i]['id']) for i in range(len(res.data['results']))]
        self.assertEqual(nearby_boxer_id_list, boxer_id_list)

        # ???????????????????????????????????????????????????
        boxer = res.data['results'][0]
        self.assertEqual(boxer['id'], int(boxer_id_list[0]))
        self.assertEqual(float(boxer['longitude']), self.club2_data['longitude'])
        self.assertEqual(float(boxer['latitude']), self.club2_data['latitude'])
        self.assertEqual(boxer['course_min_price'], self.course_data['price'])
        self.assertEqual(boxer['order_count'], 0)
        self.assertEqual(boxer['gender'], self.user_profile_data['gender'])
        self.assertEqual(boxer['avatar'], get_cdn_url(self.user_profile_data['avatar']))
        self.assertEqual(boxer['allowed_course'], self.boxer_data['allowed_course'])
        self.assertEqual(boxer['user_type'], USER_TYPE_MAP[USER_TYPE_BOXER])

        # ?????????????????????????????????
        res = self.client6.get('/nearby/boxers', data={"longitude": 116.39737,
                                                       "latitude": 40.024919,
                                                       "min_price": {self.course_data["price"]}})

        self.assertEqual(len(res.data['results']), 0)
        res = self.client6.get('/nearby/boxers', data={"longitude": 116.39737,
                                                       "latitude": 40.024919,
                                                       "min_price": {self.course_data["price"] - 1}})
        self.assertEqual(len(res.data['results']), 5)

        # ?????????????????????????????????
        res = self.client6.get('/nearby/boxers', data={"longitude": 116.39737,
                                                       "latitude": 40.024919,
                                                       "max_price": {self.course_data["price"]}})
        self.assertEqual(len(res.data['results']), 5)
        res = self.client6.get('/nearby/boxers', data={"longitude": 116.39737,
                                                       "latitude": 40.024919,
                                                       "mxn_price": {self.course_data["price"] + 1}})
        self.assertEqual(len(res.data['results']), 5)

        # ???????????????????????????
        res = self.client6.get('/nearby/boxers', data={"longitude": 116.39737,
                                                       "latitude": 40.024919,
                                                       "course_name": {self.course_data["course_name"]}})
        self.assertEqual(len(res.data['results']), 5)
        res = self.client6.get('/nearby/boxers', data={"longitude": 116.39737,
                                                       "latitude": 40.024919,
                                                       "course_name": "unknown_course"})
        self.assertEqual(len(res.data['results']), 0)

        # ??????????????????(???????????????116.39737,40.024919???????????????????????????????????????)
        res = self.client6.get('/nearby/boxers', data={"longitude": 116.39737,
                                                       "latitude": 40.024919,
                                                       "city": "?????????"})
        self.assertEqual(len(res.data['results']), 5)
        res = self.client6.get('/nearby/boxers', data={"longitude": 116.39737,
                                                       "latitude": 40.024919,
                                                       "city": "?????????"})
        self.assertEqual(len(res.data['results']), 0)

        # ?????????5??????????????????????????????
        boxer5.is_accept_order = False
        boxer5.save()
        res = self.client6.get('/nearby/boxers', data={"longitude": 116.39737,
                                                       "latitude": 40.024919,
                                                       "city": "?????????"})
        self.assertEqual(len(res.data['results']), 4)
