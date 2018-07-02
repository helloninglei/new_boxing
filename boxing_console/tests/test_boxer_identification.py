import json
from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from biz import constants, redis_client
from biz.constants import BOXER_ALLOWED_COURSES_CHOICE, USER_TYPE_BOXER
from biz.models import User, BoxerIdentification, UserProfile, OperationLog, Course, SmsLog
from biz.sms_client import SMS_TEMPLATES


class BoxerIdentificationTestCase(TestCase):
    def setUp(self):
        self.fake_user1 = User.objects.create_superuser(mobile='11111111111', password='password')
        self.fake_user2 = User.objects.create_superuser(mobile='11111111112', password='password')
        self.client = self.client_class()
        self.client.login(username=self.fake_user1, password='password')
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

    def test_boxer_change_lock_state(self):
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
        self.client.post(reverse('change_lock_state', kwargs={'pk': identification.pk,
                                                              'lock_type': constants.OperationType.BOXER_ORDER_LOCK}))
        identification = BoxerIdentification.objects.get(user=self.fake_user1)
        self.assertTrue(identification.is_locked)
        opeation_log = OperationLog.objects.get(refer_type=constants.OperationTarget.BOXER_IDENTIFICATION,
                                                refer_pk=identification.pk)
        self.assertEqual(opeation_log.operator, self.fake_user1)
        self.assertEqual(opeation_log.operation_type, constants.OperationType.BOXER_ORDER_LOCK)

        self.client.post(reverse('change_lock_state', kwargs={'pk': identification.pk,
                                                              'lock_type': constants.OperationType.BOXER_ORDER_UNLOCK}))
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
        title = "最牛的拳手"
        identification = BoxerIdentification.objects.create(**identification_data)
        redis_client.set_user_title(identification.user, title)
        self.assertEqual(self.fake_user1.boxer_identification.authentication_state,
                         constants.BOXER_AUTHENTICATION_STATE_WAITING)
        data = {'authentication_state': constants.BOXER_AUTHENTICATION_STATE_APPROVED,
                'allowed_course': [constants.BOXER_ALLOWED_COURSES_THAI_BOXING, constants.BOXER_ALLOWED_COURSES_BOXING],
                'title': title}
        res = self.client.post(reverse('identification_approve', kwargs={'pk': identification.pk}),
                               data=json.dumps(data), content_type='application/json')
        identification.refresh_from_db()
        identification.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(identification.authentication_state, constants.BOXER_AUTHENTICATION_STATE_APPROVED)
        self.assertEqual(identification.allowed_course, data['allowed_course'])
        self.assertEqual(identification.user.title, title)
        #判断审核后，是否成功添加课程
        self.assertEqual(Course.objects.filter(boxer=identification).count(), 2)

        operation_log = OperationLog.objects.get(refer_type=constants.OperationTarget.BOXER_IDENTIFICATION,
                                                 refer_pk=identification.pk)
        self.assertEqual(operation_log.operator, self.fake_user1)
        self.assertEqual(operation_log.operation_type, constants.OperationType.BOXER_AUTHENTICATION_APPROVED)
        self.assertEqual(operation_log.content, "{}".format(data['allowed_course']))
        #判断审核后，是否正确发送短信
        approve_message_log = SmsLog.objects.get(mobile=identification.mobile)
        course_dict = dict(BOXER_ALLOWED_COURSES_CHOICE)
        allowed_courses = [course_dict.get(key) for key in data['allowed_course']]
        courses = '、'.join(allowed_courses)
        self.assertEqual(approve_message_log.content, (SMS_TEMPLATES['boxerApproved']["text"]).format(courses=courses))

        self.fake_user1.refresh_from_db()
        self.assertEqual(self.fake_user1.user_type, USER_TYPE_BOXER)

    def test_boxer_identification_approve_failed_without_course(self):
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
        self.assertEqual(res.data['allowed_course'][0], "可开通的课程类型是必填项")

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
        data = {'authentication_state': constants.BOXER_AUTHENTICATION_STATE_REFUSE,
                'refuse_reason': '身份信息不全，审核不通过'}
        identification = BoxerIdentification.objects.create(**identification_data)
        res = self.client.post(reverse('identification_refuse', kwargs={'pk': identification.pk}), data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        identification = BoxerIdentification.objects.get(user=self.fake_user1)
        self.assertEqual(identification.authentication_state, constants.BOXER_AUTHENTICATION_STATE_REFUSE)
        self.assertEqual(identification.refuse_reason, data['refuse_reason'])
        opeation_log = OperationLog.objects.get(refer_type=constants.OperationTarget.BOXER_IDENTIFICATION,
                                                refer_pk=identification.pk)
        self.assertEqual(opeation_log.operator, self.fake_user1)
        self.assertEqual(opeation_log.operation_type, constants.OperationType.BOXER_AUTHENTICATION_REFUSE)
        self.assertEqual(opeation_log.content, data['refuse_reason'])

        #判断驳回审核后是否正确发送短信
        refuse_message_log = SmsLog.objects.get(mobile=identification.mobile)
        refuse_reason = data['refuse_reason']
        self.assertEqual(refuse_message_log.content, SMS_TEMPLATES['boxerRefused']["text"].format(reason=refuse_reason))

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
            elif key == 'mobile':
                self.assertEqual(response.data[key], self.fake_user1.mobile)
            else:
                self.assertEqual(response.data[key], identification_data[key])

    def create_boxer_identification_data(self):
        user_list = [User.objects.create_superuser(mobile=13000000000 + int('%d' % i), password='123')
                     for i in range(self.identification_count)]

        [UserProfile.objects.filter(user=user).update(nick_name='user{}'.format(user.pk)) for user in user_list]

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
