# -*- coding: utf-8 -*-
import datetime
import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, BoxerIdentification


class BoxerIdentificationTestCase(APITestCase):
    def setUp(self):
        self.fake_user = User.objects.create_user(mobile='mobile', password='test_password')
        self.client = self.client_class()
        self.client.login(username=self.fake_user, password='test_password')

    def test_create_identification_success(self):

        post_data = {
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
        response = self.client.post(reverse('boxer_identification'), data=post_data)
        identification = BoxerIdentification.objects.get(user=self.fake_user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in post_data:
            if key == 'birthday':
                self.assertEqual(getattr(identification, key).strftime(format("%Y-%m-%d")), post_data[key])
            else:
                self.assertEqual(getattr(identification, key), post_data[key])

    def test_create_identification_fail(self):
        post_data = {
            "real_name": "张三",
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "131313h41444141444",
            "mobile": "1313131344",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "job": 'hhh',
            "introduction": "beautiful",
            "experience": '',
            "honor_certificate_images": ['http://img1.com', 'http://img2.com', 'http://img3.com'],
            "competition_video": 'https://baidu.com'
        }
        response = self.client.post(reverse('boxer_identification'),
                                    data=json.dumps(post_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data['mobile'])
        self.assertIsNotNone(response.data['identity_number'])

    def test_create_identification_faild(self):
        post_data_without_real_name = {
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "131313141444141444",
            "mobile": "113134",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "job": 'hhh',
            "introduction": "beautiful",
            "experience": '',
            "honor_certificate_images": ['http://img1.com', 'http://img2.com', 'http://img3.com'],
            "competition_video": 'https://baidu.com'
        }

        post_data_mobile_invalid = {
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "131313141444141444",
            "mobile": "113123343334",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "job": 'hhh',
            "introduction": "beautiful",
            "experience": '',
            "honor_certificate_images": ['http://img1.com', 'http://img2.com', 'http://img3.com'],
            "competition_video": 'https://baidu.com'
        }

        response1 = self.client.post(reverse('boxer_identification'), data=post_data_without_real_name)
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)

        response2 = self.client.post(reverse('boxer_identification'), data=post_data_mobile_invalid)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_identification_with_addition_faild(self):
        post_data = {
            "real_name": "张三",
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "131313141444141444",
            "mobile": "113134",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "job": 'hhh',
            "introduction": "beautiful",
            "experience": '',
            "honor_certificate_images": ['http://img1.com', 'http://img2.com', 'http://img3.com'],
            "competition_video": ''
        }
        response = self.client.post(reverse('boxer_identification'),
                                    data=json.dumps(post_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        has_identification = BoxerIdentification.objects.filter(user=self.fake_user).exists()
        self.assertFalse(has_identification)

    def test_retrieve_identification(self):
        boxer_dentity = BoxerIdentification.objects.create(real_name='张三',
                                                           user=self.fake_user,
                                                           height=190,
                                                           weight=70,
                                                           birthday="2018-04-25",
                                                           identity_number='131313141444141444',
                                                           mobile='111111111',
                                                           is_professional_boxer=True,
                                                           club='111',
                                                           job='hhh',
                                                           introduction='hhh',
                                                           honor_certificate_images=[],
                                                           competition_video='')

        response = self.client.get(reverse('boxer_identification'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['real_name'], boxer_dentity.real_name)
        self.assertEqual(response.data['height'], boxer_dentity.height)
        self.assertEqual(response.data['weight'], boxer_dentity.weight)
        self.assertEqual(response.data['mobile'], boxer_dentity.mobile)
        self.assertEqual(response.data['identity_number'], boxer_dentity.identity_number)
        self.assertEqual(response.data['is_professional_boxer'], boxer_dentity.is_professional_boxer)
        self.assertEqual(response.data['club'], boxer_dentity.club)

    def test_update_identification(self):
        boxer_dentity = BoxerIdentification.objects.create(real_name='张三',
                                                           user=self.fake_user,
                                                           height=190,
                                                           weight=70,
                                                           birthday="2018-04-25",
                                                           identity_number='131313141444141444',
                                                           mobile='111111111',
                                                           is_professional_boxer=True,
                                                           club='111',
                                                           job='hhh',
                                                           introduction='hhh',
                                                           honor_certificate_images=[],
                                                           competition_video=''
                                                           )

        update_data = {
            "real_name": "李四",
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "131313141444141444",
            "mobile": "13134131341",
            "is_professional_boxer": True,
            "club": "c444444",
            "job": "j4444444",
            "introduction": "beautiful",
            "experience": '',
            "honor_certificate_images": ['http://img1.com', 'http://img2.com', 'http://img3.com'],
            "competition_video": 'https://baidu.com'
        }
        response = self.client.put(reverse('boxer_identification'),
                                   data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'), "存在待审核的认证信息，不能修改")

        boxer_dentity.authentication_state = constants.BOXER_AUTHENTICATION_STATE_APPROVED
        boxer_dentity.save()

        response = self.client.put(reverse('boxer_identification'),
                                   data=json.dumps(update_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.fake_user = User.objects.get(pk=self.fake_user.pk)
        for key in update_data:
            if key == 'birthday':
                self.assertEqual(getattr(self.fake_user.boxer_identification, key), datetime.date(2018, 4, 25))
            elif key == 'authentication_state':
                self.assertEqual(response.data['authentication_state'], constants.BOXER_AUTHENTICATION_STATE_WAITING)

            else:
                self.assertEqual(getattr(self.fake_user.boxer_identification, key), update_data[key])
