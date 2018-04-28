from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from biz.models import User, BoxerIdentification, UserProfile, BoxerMediaAdditional


class CoinAndMoneyTestCase(TestCase):
    def setUp(self):
        self.fake_user1 = User.objects.create_user(mobile='mobile01', password='password01')
        self.fake_user2 = User.objects.create_user(mobile='mobile02', password='password02')
        self.client = self.client_class()
        self.client.login(username=self.fake_user1, password='password01')


    def test_get_boxer_identification_list(self):
        self.create_boxer_identification_data()
        response = self.client.get(reverse('boxer_identification_list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['count'],21)
        self.assertEqual(len(response.data['results'][0]['boxer_identification_additional']), 1)

        search_nick_name_response = self.client.get(reverse('boxer_identification_list'),data={'search':'user26'})
        self.assertEqual(search_nick_name_response.data['count'],1)

        search_real_name_response = self.client.get(path='/boxer/identification?search=name5')
        self.assertEqual(search_nick_name_response.data['count'],1)



    def test_get_boxer_identification_detail(self):
        self.create_boxer_identification_data()
        response = self.client.get(reverse('boxer_identification_detail',kwargs={'pk':10}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['nike_name'])
        self.assertIsNotNone(response.data['mobile'])
        self.assertIsNotNone(response.data['birthday'])
        self.assertIsNotNone(response.data['weight'])
        self.assertIsNotNone(response.data['identity_number'])
        self.assertIsNotNone(response.data['job'])
        self.assertEqual(len(response.data['boxer_identification_additional']),1)


    def create_boxer_identification_data(self):
        user_list = [User.objects.create_user(mobile=13000000000 + int('%d' % i),password='123') for i in range(21)]

        [UserProfile.objects.create(user=user, nick_name='user{}'.format(user.pk)) for user in user_list]

        identification_list = [BoxerIdentification.objects.create(user=user,
                                                                   real_name='name{}'.format(user.pk),
                                                                   height=100 + int(user.pk),
                                                                   weight=60 + int(user.pk),
                                                                   birthday=datetime.now(),
                                                                   identity_number=111111111111111111 + int(user.pk),
                                                                   mobile=str(13000000000 + int(user.id)),
                                                                   job='job{}'.format(user.id),
                                                                   introduction='introduction{}'.format(user.id)
                                                                   )
                                   for user in user_list]

        [BoxerMediaAdditional.objects.create(boxer_identification=identification,
                                            media_url='media_url{}'.format(identification.pk),
                                            media_type='media_type{}'.format(identification.pk))
                                   for identification in identification_list]