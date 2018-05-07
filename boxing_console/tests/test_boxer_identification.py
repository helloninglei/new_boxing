from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from biz import constants
from biz.models import User, BoxerIdentification, UserProfile, OperationLog


class BoxerIdentificationTestCase(TestCase):
    def setUp(self):
        self.fake_user1 = User.objects.create_user(mobile='mobile01', password='password01')
        self.fake_user2 = User.objects.create_user(mobile='mobile02', password='password02')
        self.client = self.client_class()
        self.client.login(username=self.fake_user1, password='password01')
        self.identification_count = 20

    def test_get_boxer_identification_list(self):
        self.create_boxer_identification_data()
        list_res = self.client.get(reverse('boxer_identification_list'))
        nick_name = list_res.data['results'][-1].get('nick_name')
        real_name = list_res.data['results'][-1].get('real_name')
        BoxerIdentification.objects.get(user__user_profile__nick_name=nick_name)
        self.assertEqual(list_res.status_code, status.HTTP_200_OK)
        self.assertEqual(list_res.data['count'], self.identification_count)

        search_nick_name_res = self.client.get(reverse('boxer_identification_list'), data={'search': nick_name})
        self.assertEqual(search_nick_name_res.data['count'], 1)

        search_nick_name_fail_res = self.client.get(reverse('boxer_identification_list'), data={'search': '张三'})
        self.assertEqual(search_nick_name_fail_res.data['count'], 0)

        search_real_name_res = self.client.get(reverse('boxer_identification_list'), data={'search': real_name})
        self.assertEqual(search_real_name_res.data['count'], 1)
        search_real_name_fail_res = self.client.get(reverse('boxer_identification_list'), data={'search': '李四'})
        self.assertEqual(search_real_name_fail_res.data['count'], 0)

    def test_boxer_order_state_lock_and_unlock(self):
        identification_data = {
            "user": self.fake_user1,
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
        identification = BoxerIdentification.objects.create(**identification_data)
        self.assertFalse(self.fake_user1.boxer_identification.is_locked)
        self.client.post(reverse('boxer_order_lock', kwargs={'pk': identification.pk}))
        identification = BoxerIdentification.objects.get(user=self.fake_user1)
        self.assertTrue(identification.is_locked)
        opeation_log = OperationLog.objects.get(refer_type=constants.OperationTarget.BOXER_IDENTIFICATION,
                                                refer_pk=identification.pk)
        self.assertEqual(opeation_log.operator, self.fake_user1)
        self.assertEqual(opeation_log.operation_type, constants.OperationType.BOXER_ORDER_LOCK)

        self.client.post(reverse('boxer_order_unlock', kwargs={'pk': identification.pk}))
        self.assertFalse(self.fake_user1.boxer_identification.is_locked)
        opeation_log = OperationLog.objects.filter(refer_type=constants.OperationTarget.BOXER_IDENTIFICATION,
                                                   refer_pk=identification.pk)
        self.assertEqual(opeation_log.count(), 2)
        self.assertEqual(opeation_log.last().operation_type, constants.OperationType.BOXER_ORDER_UNLOCK)

    def test_boxer_identification_approve_success(self):
        identification_data = {
            "user": self.fake_user1,
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
        identification = BoxerIdentification.objects.create(**identification_data)

        self.assertEqual(self.fake_user1.boxer_identification.authentication_state,
                         constants.BOXER_AUTHENTICATION_STATE_WAITING)
        res = self.client.post(reverse('identification_approve', kwargs={'pk': identification.pk}),
                               data={'authentication_state': constants.BOXER_AUTHENTICATION_STATE_APPROVED,
                                     'allow_lesson': "['THAI_BOXING']"})
        identification = BoxerIdentification.objects.get(user=self.fake_user1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(identification.authentication_state, constants.BOXER_AUTHENTICATION_STATE_APPROVED)

        opeation_log = OperationLog.objects.get(refer_type=constants.OperationTarget.BOXER_IDENTIFICATION,
                                                refer_pk=identification.pk)
        self.assertEqual(opeation_log.operator, self.fake_user1)
        self.assertEqual(opeation_log.operation_type, constants.OperationType.BOXER_AUTHENTICATION_APPROVED)

    def test_boxer_identification_approve_failed_without_lesson(self):
        identification_data = {
            "user": self.fake_user1,
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
        identification = BoxerIdentification.objects.create(**identification_data)
        res = self.client.post(reverse('identification_approve', kwargs={'pk': identification.pk}),
                               data={'authentication_state': constants.BOXER_AUTHENTICATION_STATE_APPROVED})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['allow_lesson'][0], "可开通的课程类型是必填项")

    def test_boxer_identification_refuse_success(self):
        identification_data = {
            "user": self.fake_user1,
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
        identification = BoxerIdentification.objects.create(**identification_data)
        res = self.client.post(reverse('identification_refuse', kwargs={'pk': identification.pk}),
                               data={'authentication_state': constants.BOXER_AUTHENTICATION_STATE_REFUSE,
                                     'refuse_reason': '身份信息不全，审核不通过'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        identification = BoxerIdentification.objects.get(user=self.fake_user1)
        self.assertEqual(identification.authentication_state, constants.BOXER_AUTHENTICATION_STATE_REFUSE)
        self.assertEqual(identification.refuse_reason, '身份信息不全，审核不通过')
        opeation_log = OperationLog.objects.get(refer_type=constants.OperationTarget.BOXER_IDENTIFICATION,
                                                refer_pk=identification.pk)
        self.assertEqual(opeation_log.operator, self.fake_user1)
        self.assertEqual(opeation_log.operation_type, constants.OperationType.BOXER_AUTHENTICATION_REFUSE)
        self.assertEqual(opeation_log.content, '拳手认证信息审核失败，理由是：身份信息不全，审核不通过')

    def test_boxer_identification_refuse_faild_without_reason(self):
        identification_data = {
            "user": self.fake_user1,
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
        identification = BoxerIdentification.objects.create(**identification_data)
        res = self.client.post(reverse('identification_refuse', kwargs={'pk': identification.pk}),
                               data={'authentication_state': constants.BOXER_AUTHENTICATION_STATE_REFUSE})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['refuse_reason'][0], '驳回理由是必填项')

    def test_get_boxer_identification_detail(self):
        identification_data = {
                                "user": self.fake_user1,
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
        identification_detail = BoxerIdentification.objects.create(**identification_data)
        response = self.client.get(reverse('boxer_identification_detail', kwargs={'pk': identification_detail.pk}))
        for key in identification_data.keys():
            if key == 'user':
                self.assertEqual(response.data[key], self.fake_user1.pk)
            else:
                self.assertEqual(response.data[key], identification_data[key])

    def create_boxer_identification_data(self):
        user_list = [User.objects.create_user(mobile=13000000000 + int('%d' % i), password='123')
                     for i in range(self.identification_count)]

        [UserProfile.objects.create(user=user, nick_name='user{}'.format(user.pk)) for user in user_list]

        [BoxerIdentification.objects.create(
            user=user,
            real_name='name{}'.format(user.pk),
            height=100 + int(user.pk),
            weight=60 + int(user.pk),
            birthday=datetime.now(),
            identity_number=111111111111111111 + int(user.pk),
            mobile=str(13000000000 + int(user.id)),
            job='job{}'.format(user.id),
            introduction='introduction{}'.format(user.id),
            honor_certificate_images=['http://img{}.com'.format(user.id)],
            competition_video='https://baidu{}.com'.format(user.id))
            for user in user_list]
