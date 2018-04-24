# -*- coding: utf-8 -*-
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from biz import constants
from biz.models import User, CoinChangeLog, MoneyChangeLog


class CoinAndMoneyTestCase(TestCase):
    def setUp(self):
        self.fake_user1 = User.objects.create_user(mobile='mobile01', password='password01')
        self.fake_user2 = User.objects.create_user(mobile='mobile02', password='password02')
        self.client = self.client_class()
        self.client.login(username=self.fake_user1, password='password01')

    def test_add_coin_amount_success(self):
        responst = self.client.post(reverse('coin_add_or_substract', kwargs={'effect_user_id':self.fake_user2.pk}),
                                    HTTP_OPERATION=constants.COIN_CHANGE_TYPE_INCREASE_RECHARGE,
                                    data={'change_amount':100,})
        self.assertEqual(responst.status_code, status.HTTP_200_OK)

        coin_log = CoinChangeLog.objects.filter(user=self.fake_user2).first()
        self.assertEqual(coin_log.last_amount, 0)
        self.assertEqual(coin_log.change_amount, 100)
        self.assertEqual(coin_log.remain_amount, 100)
        self.assertEqual(coin_log.operator, self.fake_user1.mobile)
        self.assertEqual(coin_log.change_type, u'INCREASE_COIN_RECHARGE')

    def test_add_coin_amount_failed(self):
        responst1 = self.client.post(reverse('coin_add_or_substract', kwargs={'effect_user_id': self.fake_user1.pk}),
                                    data={'change_amount': 100})
        self.assertEqual(responst1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(responst1.data['error_message'][0], u'拳豆修改类型未知')

        responst2 = self.client.post(reverse('coin_add_or_substract', kwargs={'effect_user_id': self.fake_user1.pk}),
                                     HTTP_OPERATION='INCREASE_COIN_RECHARGE',
                                     data={})
        self.assertEqual(responst2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNot(self,CoinChangeLog.objects.filter(user=self.fake_user1).exists())

    def test_add_money_success(self):
        responst = self.client.post(reverse('money_add_or_substract', kwargs={'effect_user_id': self.fake_user2.pk}),
                                    HTTP_OPERATION=constants.MONEY_CHANGE_TYPE_INCREASE_ORDER,
                                    data={'change_amount': 100,})
        self.assertEqual(responst.status_code, status.HTTP_200_OK)

        money_log = MoneyChangeLog.objects.filter(user=self.fake_user2).first()
        self.assertEqual(money_log.last_amount, 0)
        self.assertEqual(money_log.change_amount, 100*100)
        self.assertEqual(money_log.remain_amount, 100*100)
        self.assertEqual(money_log.operator, self.fake_user1.mobile)
        self.assertEqual(money_log.change_type, constants.MONEY_CHANGE_TYPE_INCREASE_ORDER)

    def test_add_money_failed(self):
        responst1 = self.client.post(reverse('money_add_or_substract', kwargs={'effect_user_id': self.fake_user2.pk}),
                                     HTTP_OPERATION=constants.MONEY_CHANGE_TYPE_INCREASE_ORDER,
                                     data={})
        self.assertEqual(responst1.status_code, status.HTTP_400_BAD_REQUEST)

        responst2 = self.client.post(reverse('money_add_or_substract', kwargs={'effect_user_id': self.fake_user2.pk}),
                                     data={'change_amount': 100})
        self.assertEqual(responst2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(responst2.data['error_message'][0], u'钱包余额修改类型未知')
