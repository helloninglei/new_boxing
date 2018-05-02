# -*- coding: utf-8 -*-
import datetime
import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, BoxerIdentification, BoxerMediaAdditional


class BoxerIdentificationTestCase(APITestCase):
    def setUp(self):
        self.fake_user = User.objects.create_user(mobile='mobile', password='test_password')
        self.client = self.client_class()
        self.client.login(username=self.fake_user, password='test_password')

    def test_create_identification_without_addition_success(self):

        post_data = {
                    "real_name": "张三",
                    "height": 190,
                    "weight": 120,
                    "birthday": "2018-04-25",
                    "identity_number": "131313141444",
                    "mobile": "113134",
                    "is_professional_boxer": True,
                    "club": "131ef2f3",
                    "job": 'hhh',
                    "introduction": "beautiful",
                    "experience": '',
                    "boxer_identification_additional": []
                }
        response = self.client.post(reverse('boxer_identification'),data=post_data)
        identification = BoxerIdentification.objects.filter(user=self.fake_user).first()
        identification_addition = BoxerMediaAdditional.objects.filter(boxer_identification=identification).first()

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIsNotNone(identification)
        self.assertEqual(identification.real_name, '张三')
        self.assertEqual(identification.height, 190)
        self.assertEqual(identification.weight, 120)
        self.assertEqual(identification.identity_number, '131313141444')
        self.assertEqual(identification.mobile, '113134')
        self.assertEqual(identification.is_professional_boxer, True)
        self.assertEqual(identification.club, '131ef2f3')
        self.assertEqual(identification.introduction, 'beautiful')
        self.assertEqual(identification.experience, '')
        self.assertIsNone(identification_addition)

    def test_create_identification_with_addition_success(self):
        post_data = {
            "real_name": "张三",
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "131313141444",
            "mobile": "113134",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "job":'hhh',
            "introduction": "beautiful",
            "experience": '',
            "boxer_identification_additional": [{"media_url":"http://img1.com","media_type": constants.IMAGE_CERTIFICATE_OF_HONOR},
                                                {"media_url": "http://img2.com", "media_type": constants.IMAGE_CERTIFICATE_OF_HONOR},
                                                {"media_url": "http://img3.com", "media_type": constants.IMAGE_CERTIFICATE_OF_HONOR}
                                                ]
        }
        response = self.client.post(reverse('boxer_identification'),
                                    data=json.dumps(post_data), content_type='application/json')

        fake_user_identification = self.fake_user.boxer_identification
        fake_user_addition = self.fake_user.boxer_identification.boxer_identification_additional

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIsNotNone(fake_user_identification)
        self.assertIsNotNone(fake_user_addition)

        for key in post_data:
            if key == 'birthday':
                self.assertEqual(getattr(fake_user_identification, key), datetime.date(2018, 4, 25))
            elif key =='boxer_identification_additional':
                pass
            else:
                self.assertEqual(getattr(fake_user_identification,key), post_data[key])

        self.assertEqual(fake_user_addition.all().count(),len(post_data['boxer_identification_additional']))
        for count in range(fake_user_addition.all().count()):
            self.assertEqual(fake_user_addition.all()[count].media_url, post_data['boxer_identification_additional'][count]['media_url'])
            self.assertEqual(fake_user_addition.all()[count].media_type, post_data['boxer_identification_additional'][count]['media_type'])

    def test_create_identification_faild(self):
        post_data_without_real_name = {
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "131313141444",
            "mobile": "113134",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "job": 'hhh',
            "introduction": "beautiful",
            "experience": '',
            "boxer_identification_additional": []
        }

        post_data_mobile_invalid = {
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "131313141444",
            "mobile": "113123343334",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "job": 'hhh',
            "introduction": "beautiful",
            "experience": '',
            "boxer_identification_additional": []
        }


        response1 = self.client.post(reverse('boxer_identification'), data=post_data_without_real_name)
        self.assertEqual(response1.status_code,status.HTTP_400_BAD_REQUEST)

        response2 = self.client.post(reverse('boxer_identification'), data=post_data_mobile_invalid)
        self.assertEqual(response2.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_identification_with_addition_faild(self):
        post_data = {
            "real_name": "张三",
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "131313141444",
            "mobile": "113134",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "job": 'hhh',
            "introduction": "beautiful",
            "experience": '',
            "boxer_identification_additional": [{"media_url":"http://img1.com","media_type": 'hhh'},
                                                {"media_url": "http://img2.com", "media_type": constants.IMAGE_CERTIFICATE_OF_HONOR},
                                                {"media_url": "http://img3.com", "media_type": constants.IMAGE_CERTIFICATE_OF_HONOR}
                                                ]
        }
        response = self.client.post(reverse('boxer_identification'),
                                    data=json.dumps(post_data), content_type='application/json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        identification = BoxerIdentification.objects.filter(user=self.fake_user).first()
        self.assertIsNone(identification)

    def test_retrieve_identification(self):
        boxer_dentity = BoxerIdentification.objects.create(real_name='张三',
                                                           user=self.fake_user,
                                                            height=190,
                                                            weight=70,
                                                            birthday="2018-04-25",
                                                            identity_number='111111111111111',
                                                            mobile='111111111',
                                                            is_professional_boxer=True,
                                                            club='111',
                                                            job='hhh',
                                                            introduction='hhh')

        BoxerMediaAdditional.objects.create(boxer_identification=boxer_dentity,
                                             media_url='http://img1.com',
                                             media_type=constants.IMAGE_CERTIFICATE_OF_HONOR)

        response = self.client.get(reverse('boxer_identification'))

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['real_name'], '张三')
        self.assertEqual(response.data['height'], 190)
        self.assertEqual(response.data['weight'], 70)
        self.assertEqual(response.data['mobile'], '111111111')
        self.assertEqual(response.data['identity_number'], '111111111111111')
        self.assertEqual(response.data['is_professional_boxer'], True)
        self.assertEqual(response.data['club'], '111')
        self.assertEqual(response.data['boxer_identification_additional'][0]['media_type'],constants.IMAGE_CERTIFICATE_OF_HONOR)
        self.assertEqual(response.data['boxer_identification_additional'][0]['media_url'], 'http://img1.com')


    def test_update_identification(self):
        boxer_dentity = BoxerIdentification.objects.create(real_name='张三',
                                                           user=self.fake_user,
                                                           height=190,
                                                           weight=70,
                                                           birthday="2018-04-25",
                                                           identity_number='111111111111111',
                                                           mobile='111111111',
                                                           is_professional_boxer=True,
                                                           club='111',
                                                           job='hhh',
                                                           introduction='hhh')

        BoxerMediaAdditional.objects.create(boxer_identification=boxer_dentity,
                                            media_url='http://img1.com',
                                            media_type=constants.IMAGE_CERTIFICATE_OF_HONOR)

        update_data = {
            "real_name": "李四",
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "im444444",
            "mobile": "m4444444",
            "is_professional_boxer": True,
            "club": "c444444",
            "job": "j4444444",
            "introduction": "beautiful",
            "experience": '',
            "boxer_identification_additional": [
                                                {"media_url": "http://img11.com",
                                                 "media_type": constants.VIDEO_CONTESTANT},
                                                {"media_url": "http://img22.com",
                                                 "media_type": constants.IMAGE_CERTIFICATE_OF_HONOR}
                                                ]
        }
        response = self.client.put(reverse('boxer_identification'),
                                      data=json.dumps(update_data),
                                      content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['real_name'], '李四')
        self.assertEqual(response.data['height'], 190)
        self.assertEqual(response.data['weight'], 120)
        self.assertEqual(response.data['mobile'], 'm4444444')
        self.assertEqual(response.data['identity_number'], 'im444444')
        self.assertEqual(response.data['is_professional_boxer'], True)
        self.assertEqual(response.data['club'], 'c444444')
        self.assertEqual(response.data['job'], 'j4444444')
        self.assertEqual(len(response.data['boxer_identification_additional']),2)
        self.assertEqual(response.data['boxer_identification_additional'][0]['media_type'],
                         constants.VIDEO_CONTESTANT)
        self.assertEqual(response.data['boxer_identification_additional'][0]['media_url'], 'http://img11.com')
        self.assertEqual(response.data['boxer_identification_additional'][1]['media_type'],
                         constants.IMAGE_CERTIFICATE_OF_HONOR)
        self.assertEqual(response.data['boxer_identification_additional'][1]['media_url'], 'http://img22.com')
