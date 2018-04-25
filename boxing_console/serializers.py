# -*- coding: utf-8 -*-
import math
from rest_framework import serializers

from biz.models import CoinChangeLog, User, MoneyChangeLog
from biz import models, constants


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['nick_name', 'gender', 'address', 'name', 'nation', 'birthday', 'height', 'weight', 'profession']

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H-%M-%S')
    user_basic_info = serializers.SerializerMethodField()

    def get_user_basic_info(self, instance):
        if hasattr(instance, 'user_profile'):
            return UserProfileSerializer(instance.user_profile).data

    class Meta:
        model = models.User
        fields = ['id', 'username', 'mobile', 'date_joined', 'user_basic_info']


class CoinLogSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format('%Y-%m-%d %H:%M:%S'),required=False)
    change_type = serializers.ChoiceField(choices=constants.COIN_CHANGE_TYPE_CHOICES,
                                          error_messages={'invalid_choice': u'拳豆修改类型未知'})

    def create(self, validated_data):
        user = validated_data['user']
        change_amount = validated_data['change_amount']
        last_amount = user.coin_balance
        remain_amount = last_amount + change_amount
        operator = self.context['request'].user
        user.coin_balance += change_amount
        user.save()

        coin_change_log = CoinChangeLog.objects.create(last_amount=last_amount,
                                                       operator=operator,
                                                       remain_amount=remain_amount,
                                                       **validated_data)

        return coin_change_log


    class Meta:
        model = CoinChangeLog
        fields = '__all__'

class MoneyLogSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format('%Y-%m-%d %H:%M:%S'), required=False)
    change_type = serializers.ChoiceField(choices=constants.MONEY_CHANGE_TYPE_CHOICES,
                                          error_messages={'invalid_choice': u'钱包余额修改类型未知'})


    def create(self, validated_data):
        user = validated_data['user']
        change_amount = validated_data['change_amount']
        last_amount = user.money_balance
        remain_amount = last_amount + change_amount
        operator = self.context['request'].user
        user.money_balance += change_amount
        user.save()

        money_change_log = MoneyChangeLog.objects.create(last_amount=last_amount,
                                                       operator=operator,
                                                       remain_amount=remain_amount,
                                                       **validated_data)

        return money_change_log


    class Meta:
        model = MoneyChangeLog
        fields = '__all__'