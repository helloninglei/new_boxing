# -*- coding: utf-8 -*-
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from biz import constants
from biz.models import User, CoinChangeLog


class CoinAndMoneyTestCase(TestCase):
    def setUp(self):
        self.fake_user1 = User.objects.create_superuser(mobile='11111111111', password='password01')
        self.fake_user2 = User.objects.create_superuser(mobile='11111111112', password='password02')
        self.client = self.client_class()
        self.client.login(username=self.fake_user1, password='password01')

    def test_add_coin_amount_success(self):
        responst = self.client.post(reverse('coin_change'),data={'change_amount':100,
                                                                 'user':self.fake_user2.pk,
                                                                 'change_type':constants.COIN_CHANGE_TYPE_INCREASE_RECHARGE})
        self.assertEqual(responst.status_code, status.HTTP_201_CREATED)

        coin_log = CoinChangeLog.objects.filter(user=self.fake_user2).first()
        self.assertEqual(coin_log.last_amount, 0)
        self.assertEqual(coin_log.change_amount, 100)
        self.assertEqual(coin_log.remain_amount, 100)
        self.assertEqual(coin_log.operator, self.fake_user1)
        self.assertEqual(coin_log.change_type, constants.COIN_CHANGE_TYPE_INCREASE_RECHARGE)

    def test_add_coin_amount_failed(self):
        responst1 = self.client.post(reverse('coin_change'),data={'change_amount': 100,
                                                                  'user': self.fake_user1.pk,
                                                                  'change_type':'hhh'})
        self.assertEqual(responst1.status_code, status.HTTP_400_BAD_REQUEST)

        responst2 = self.client.post(reverse('coin_change'),
                                     data={'user':self.fake_user1,
                                           'change_type':constants.MONEY_CHANGE_TYPE_INCREASE_RECHARGE})
        self.assertEqual(responst2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNot(self,CoinChangeLog.objects.filter(user=self.fake_user1).exists())
