# -*- coding: utf-8 -*-
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
                    "birthday": "2018-04-25T11:04:40.634170+08:00",
                    "identity_number": "131313141444",
                    "mobile": "113134",
                    "is_professional_boxer": True,
                    "club": "131ef2f3",
                    "introduction": "beautiful",
                    "experience": '',
                    "boxer_identification_additional": []
                }
        response = self.client.post(reverse('identification_create'),data=post_data)
        identification = BoxerIdentification.objects.filter(user=self.fake_user).first()
        identification_addition = BoxerMediaAdditional.objects.filter(boxer_identification=identification).first()

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIsNotNone(identification)
        self.assertEqual(identification.real_name, u'张三')
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
            "birthday": "2018-04-25T11:04:40.634170+08:00",
            "identity_number": "131313141444",
            "mobile": "113134",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "introduction": "beautiful",
            "experience": '',
            "boxer_identification_additional": [{"media_url":"url0","media_type": constants.IMAGE_CERTIFICATE_OF_HONOR},
                                                {"media_url": "url1", "media_type": constants.IMAGE_CERTIFICATE_OF_HONOR},
                                                {"media_url": "url2", "media_type": constants.IMAGE_CERTIFICATE_OF_HONOR}
                                                ]
        }
        response = self.client.post(reverse('identification_create'),
                                    data=json.dumps(post_data), content_type='application/json')
        identification = BoxerIdentification.objects.filter(user=self.fake_user).first()
        identification_addition = BoxerMediaAdditional.objects.filter(boxer_identification=identification)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(identification)
        self.assertEqual(identification.real_name, u'张三')
        self.assertEqual(identification.height, 190)
        self.assertEqual(identification.weight, 120)
        self.assertEqual(identification.identity_number, '131313141444')
        self.assertEqual(identification.mobile, '113134')
        self.assertEqual(identification.is_professional_boxer, True)
        self.assertEqual(identification.club, '131ef2f3')
        self.assertEqual(identification.introduction, 'beautiful')
        self.assertEqual(identification.experience, '')

        self.assertIsNotNone(identification_addition)
        self.assertEqual(len(identification_addition),3)
        self.assertEqual(identification_addition[0].media_url, 'url0')
        self.assertEqual(identification_addition[0].media_type, constants.IMAGE_CERTIFICATE_OF_HONOR)

    def test_create_identification_faild(self):
        post_data_without_real_name = {
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25T11:04:40.634170+08:00",
            "identity_number": "131313141444",
            "mobile": "113134",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "introduction": "beautiful",
            "experience": '',
            "boxer_identification_additional": []
        }

        post_data_mobile_invalid = {
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25T11:04:40.634170+08:00",
            "identity_number": "131313141444",
            "mobile": "113123343334",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "introduction": "beautiful",
            "experience": '',
            "boxer_identification_additional": []
        }


        response1 = self.client.post(reverse('identification_create'), data=post_data_without_real_name)
        self.assertEqual(response1.status_code,status.HTTP_400_BAD_REQUEST)

        response2 = self.client.post(reverse('identification_create'), data=post_data_mobile_invalid)
        self.assertEqual(response2.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_identification_with_addition_faild(self):
        post_data = {
            "real_name": "张三",
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25T11:04:40.634170+08:00",
            "identity_number": "131313141444",
            "mobile": "113134",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "introduction": "beautiful",
            "experience": '',
            "boxer_identification_additional": [{"media_url":"url0","media_type": 'hhh'},
                                                {"media_url": "url1", "media_type": constants.IMAGE_CERTIFICATE_OF_HONOR},
                                                {"media_url": "url2", "media_type": constants.IMAGE_CERTIFICATE_OF_HONOR}
                                                ]
        }
        response = self.client.post(reverse('identification_create'),
                                    data=json.dumps(post_data), content_type='application/json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        identification = BoxerIdentification.objects.filter(user=self.fake_user).first()
        self.assertIsNone(identification)

    def test_retrieve_identification(self):
        boxer_dentity = BoxerIdentification.objects.create(real_name='张三',
                                                           user=self.fake_user,
                                                            height=190,
                                                            weight=70,
                                                            birthday="2018-04-25T11:04:40.634170+08:00",
                                                            identity_number='111111111111111',
                                                            mobile='111111111',
                                                            is_professional_boxer=True,
                                                            club='111',
                                                            introduction='hhh')

        BoxerMediaAdditional.objects.create(boxer_identification=boxer_dentity,
                                             media_url='url0',
                                             media_type=constants.IMAGE_CERTIFICATE_OF_HONOR)

        response = self.client.get(reverse('get_boxer_identification'))

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['real_name'], u'张三')
        self.assertEqual(response.data['height'], 190)
        self.assertEqual(response.data['weight'], 70)
        self.assertEqual(response.data['mobile'], '111111111')
        self.assertEqual(response.data['identity_number'], '111111111111111')
        self.assertEqual(response.data['is_professional_boxer'], True)
        self.assertEqual(response.data['club'], '111')

        self.assertEqual(response.data['boxer_identification_additional'][0]['media_type'],constants.IMAGE_CERTIFICATE_OF_HONOR)
        self.assertEqual(response.data['boxer_identification_additional'][0]['media_url'], 'url0')