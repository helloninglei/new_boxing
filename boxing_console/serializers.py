# -*- coding: utf-8 -*-
import math
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
    change_amount = serializers.IntegerField()
    change_type = serializers.CharField()
    user = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user_id = self.context['request'].parser_context['kwargs'].get('user_id')
        user = User.objects.filter(pk=user_id).first()
        if not user:
            raise serializers.ValidationError({'error_message': '用户不存在'})
        attrs['user'] = user
        attrs['last_amount'] = user.coin_balance
        attrs['operator'] = self.context['request'].user
        attrs['remain_amount'] = attrs['last_amount'] + attrs['change_amount']
        if attrs['change_type'] not in dict(constants.COIN_CHANGE_TYPE_CHOICES).keys():
            raise ValidationError({'error_message': '拳豆修改类型未知'})
        return attrs

    def create(self, validated_data):
        coin_change_log = CoinChangeLog.objects.create(**validated_data)
        user = validated_data['user']
        user.coin_balance += validated_data['change_amount']
        user.save()
        return coin_change_log


    class Meta:
        model = CoinChangeLog
        fields = '__all__'

class MoneyLogSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format('%Y-%m-%d %H:%M:%S'), required=False)
    change_amount = serializers.IntegerField()
    change_type = serializers.CharField()
    user = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user_id = self.context['request'].parser_context['kwargs'].get('user_id')
        user = User.objects.filter(pk=user_id).first()
        if not user:
            raise serializers.ValidationError({'error_message': '用户不存在'})
        attrs['user'] = user
        attrs['last_amount'] = user.money_balance
        # attrs['change_amount'] = int(math.floor(attrs['change_amount'] * 100))
        attrs['remain_amount'] = attrs['last_amount'] + attrs['change_amount']
        attrs['operator'] = self.context['request'].user
        if attrs['change_type'] not in dict(constants.MONEY_CHANGE_TYPE_CHOICES).keys():
            raise serializers.ValidationError({'error_message': '钱包余额修改类型未知'})
        return attrs

    def create(self, validated_data):
        money_change_log = MoneyChangeLog.objects.create(**validated_data)
        user = validated_data['user']
        user.money_balance += validated_data['change_amount']
        user.save()
        return money_change_log

    class Meta:
        model = MoneyChangeLog
        fields = '__all__'