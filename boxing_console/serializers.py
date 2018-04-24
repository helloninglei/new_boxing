# -*- coding: utf-8 -*-
import math
from rest_framework import serializers
from biz.models import CoinChangeLog
from biz import models, constants
from biz.services import coin_money_handle


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


class CoinLogListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format('%Y-%m-%d %H:%M:%S'))

    class Meta:
        model = CoinChangeLog
        fields = '__all__'

class CoinSubstractSerializer(serializers.Serializer):
    change_type = serializers.SerializerMethodField()
    change_amount = serializers.IntegerField()
    effect_user = serializers.SerializerMethodField()
    operator = serializers.SerializerMethodField(required=False)
    remarks = serializers.SerializerMethodField(required=False)

    def validate(self, attrs):
        attrs['change_type'] = self.context['request'].META.get('HTTP_OPERATION')
        attrs['operator'] = self.context['request'].user
        attrs['effect_user'] = self.context['request'].parser_context['kwargs'].get('effect_user_id')

        if attrs['change_type'] not in dict(constants.COIN_CHANGE_TYPE_CHOICES).keys():
            raise serializers.ValidationError({'error_message': '拳豆修改类型未知'})
        return attrs

    def get_change_type(self):
        return self.validated_data['change_type']

    def get_change_amount(self):
        return self.validated_data['change_amount']

    def get_effect_user(self):
        return self.validated_data['effect_user']

    def get_operator(self):
        return self.validated_data['operator']

    def get_remarks(self):
        return self.validated_data['remarks']

    def create(self, validated_data):
        return coin_money_handle.coin_handle(**validated_data)


class MoneySubstractSerializer(serializers.Serializer):
    change_type = serializers.SerializerMethodField()
    change_amount = serializers.FloatField()
    effect_user = serializers.SerializerMethodField()
    operator = serializers.SerializerMethodField(required=False)
    remarks = serializers.SerializerMethodField(required=False)

    def validate(self, attrs):
        attrs['change_type'] = self.context['request'].META.get('HTTP_OPERATION')
        attrs['operator'] = self.context['request'].user
        attrs['effect_user'] = self.context['request'].parser_context['kwargs'].get('effect_user_id')
        attrs['change_amount'] = self.context['request'].data.get('change_amount')

        if attrs['change_type'] not in dict(constants.MONEY_CHANGE_TYPE_CHOICES).keys():
            raise serializers.ValidationError({'error_message': '钱包余额修改类型未知'})
        else:
            attrs['change_amount'] = int(math.floor(float(attrs['change_amount'])*100))
        return attrs

    def get_change_type(self):
        return self.validated_data['change_type']

    def get_change_amount(self):
        return self.validated_data['change_amount']

    def get_effect_user(self):
        return self.validated_data['effect_user']

    def get_operator(self):
        return self.validated_data['operator']

    def get_remarks(self):
        return self.validated_data['remarks']

    def create(self, validated_data):
        return coin_money_handle.money_handle(**validated_data)