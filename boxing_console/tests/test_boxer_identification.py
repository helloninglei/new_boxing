from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from biz.models import User, BoxerIdentification, UserProfile


class CoinAndMoneyTestCase(TestCase):
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
        get_by_nick_name = BoxerIdentification.objects.get(user__user_profile__nick_name=nick_name)
        self.assertEqual(list_res.status_code,status.HTTP_200_OK)
        self.assertEqual(list_res.data['count'],self.identification_count)

        search_nick_name_res = self.client.get(reverse('boxer_identification_list'),data={'search': nick_name})
        self.assertEqual(search_nick_name_res.data['count'],1)
        search_result = search_nick_name_res.data['results'][0]
        self.assertEqual(search_result.get('real_name'), get_by_nick_name.real_name)
        self.assertEqual(search_result.get('height'), get_by_nick_name.height)
        self.assertEqual(search_result.get('weight'), get_by_nick_name.weight)
        self.assertEqual(search_result.get('birthday'), get_by_nick_name.birthday.strftime(format("%Y-%m-%d")))
        self.assertEqual(search_result.get('is_professional_boxer'), get_by_nick_name.is_professional_boxer)
        self.assertEqual(search_result.get('club'), get_by_nick_name.club)
        self.assertEqual(search_result.get('job'), get_by_nick_name.job)
        self.assertEqual(search_result.get('introduction'), get_by_nick_name.introduction)
        self.assertEqual(search_result.get('lock_state'), get_by_nick_name.lock_state)
        self.assertEqual(search_result.get('experience'), get_by_nick_name.experience)
        self.assertEqual(search_result.get('authentication_state'), get_by_nick_name.authentication_state)
        self.assertEqual(search_result.get('honor_certificate_images'), get_by_nick_name.honor_certificate_images)
        self.assertEqual(search_result.get('competition_video'), get_by_nick_name.competition_video)

        search_real_name_res = self.client.get(reverse('boxer_identification_list'), data={'search': real_name})
        self.assertEqual(search_real_name_res.data['count'],1)
        search_result = search_real_name_res.data['results'][0]
        self.assertEqual(search_result.get('real_name'), get_by_nick_name.real_name)
        self.assertEqual(search_result.get('height'), get_by_nick_name.height)
        self.assertEqual(search_result.get('weight'), get_by_nick_name.weight)
        self.assertEqual(search_result.get('birthday'), get_by_nick_name.birthday.strftime(format("%Y-%m-%d")))
        self.assertEqual(search_result.get('is_professional_boxer'), get_by_nick_name.is_professional_boxer)
        self.assertEqual(search_result.get('club'), get_by_nick_name.club)
        self.assertEqual(search_result.get('job'), get_by_nick_name.job)
        self.assertEqual(search_result.get('introduction'), get_by_nick_name.introduction)
        self.assertEqual(search_result.get('lock_state'), get_by_nick_name.lock_state)
        self.assertEqual(search_result.get('experience'), get_by_nick_name.experience)
        self.assertEqual(search_result.get('authentication_state'), get_by_nick_name.authentication_state)
        self.assertEqual(search_result.get('honor_certificate_images'), get_by_nick_name.honor_certificate_images)
        self.assertEqual(search_result.get('competition_video'), get_by_nick_name.competition_video)

    def test_get_boxer_identification_detail(self):
        self.create_boxer_identification_data()
        list_res = self.client.get(reverse('boxer_identification_list'))
        pk = list_res.data['results'][-1].get('id')
        identification = BoxerIdentification.objects.get(pk=pk)
        response = self.client.get(reverse('boxer_identification_detail',kwargs={'pk':pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nick_name'], identification.user.user_profile.nick_name)
        self.assertEqual(response.data['mobile'], identification.mobile)
        self.assertEqual(response.data['birthday'], identification.birthday.strftime(format("%Y-%m-%d")))
        self.assertEqual(response.data['weight'], identification.weight)
        self.assertEqual(response.data['identity_number'], identification.identity_number)
        self.assertEqual(response.data['job'], identification.job)
        self.assertEqual(response.data['introduction'], identification.introduction)
        self.assertEqual(response.data['lock_state'], identification.lock_state)
        self.assertEqual(response.data['experience'], identification.experience)
        self.assertEqual(response.data['authentication_state'], identification.authentication_state)



    def create_boxer_identification_data(self):
        user_list = [User.objects.create_user(mobile=13000000000 + int('%d' % i),password='123')
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
            honor_certificate_images=['http://img{}.com'.format(user.id),],
            competition_video='https://baidu{}.com'.format(user.id))
            for user in user_list]
