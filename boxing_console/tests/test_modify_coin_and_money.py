# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, CoinChangeLog, MoneyChangeLog


class CoinAndMoneyTestCase(APITestCase):
    def setUp(self):
        self.fake_user1 = User.objects.create_user(mobile='mobile01', password='password01')
        self.fake_user2 = User.objects.create_user(mobile='mobile02', password='password02')
        self.client = self.client_class()
        self.client.login(username=self.fake_user1, password='password01')

    def test_add_coin_amount_success(self):
        responst = self.client.post(reverse('add_coin', kwargs={'effect_user_id':self.fake_user2.pk}),
                                   data={'change_amount':100,
                                         'change_type':'INCREASE_COIN_RECHARGE'})
        self.assertEqual(responst.status_code, status.HTTP_200_OK)

        coin_log = CoinChangeLog.objects.filter(user=self.fake_user2).first()
        self.assertEqual(coin_log.lastAmount, 0)
        self.assertEqual(coin_log.changeAmount, 100)
        self.assertEqual(coin_log.remainAmount, 100)
        self.assertEqual(int(coin_log.operator), self.fake_user1.pk)
        self.assertEqual(coin_log.change_type, u'INCREASE_COIN_RECHARGE')

    def test_add_coin_amount_failed(self):
        responst1 = self.client.post(reverse('add_coin', kwargs={'effect_user_id': self.fake_user1.pk}),
                                    data={'change_amount': 100})
        self.assertEqual(responst1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(responst1.data['message'], u'拳豆变动类型未知')

        responst2 = self.client.post(reverse('add_coin', kwargs={'effect_user_id': self.fake_user1.pk}),
                                      data={'change_type':'INCREASE_COIN_RECHARGE'})
        self.assertEqual(responst2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(responst2.data['message'], u'请输入需要增加或减少的拳豆值')
        self.assertIsNot(self,CoinChangeLog.objects.filter(user=self.fake_user1).exists())

    def test_add_money_success(self):
        responst = self.client.post(reverse('add_money', kwargs={'effect_user_id': self.fake_user2.pk}),
                                    data={'change_amount': 100,
                                          'change_type': constants.MONEY_CHANGE_TPYE_INCREASE_RECHARGE})
        self.assertEqual(responst.status_code, status.HTTP_200_OK)

        money_log = MoneyChangeLog.objects.filter(user=self.fake_user2).first()
        self.assertEqual(money_log.lastAmount, 0)
        self.assertEqual(money_log.changeAmount, 100)
        self.assertEqual(money_log.remainAmount, 100*100)
        self.assertEqual(int(money_log.operator), self.fake_user1.pk)
        self.assertEqual(money_log.change_type, constants.MONEY_CHANGE_TPYE_INCREASE_RECHARGE)

    def test_add_money_failed(self):
        responst1 = self.client.post(reverse('add_money', kwargs={'effect_user_id': self.fake_user2.pk}),
                                    data={'change_type': constants.MONEY_CHANGE_TPYE_INCREASE_RECHARGE})
        self.assertEqual(responst1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(responst1.data['message'], u'请输入需要增加或减少的钱包金额')

        responst2 = self.client.post(reverse('add_money', kwargs={'effect_user_id': self.fake_user2.pk}),
                                     data={'change_amount': 100})
        self.assertEqual(responst2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(responst2.data['message'], u'钱包金额变动类型未知')
