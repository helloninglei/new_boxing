# -*- coding: utf-8 -*-
from rest_framework import serializers

from biz.models import CoinChangeLog, MoneyChangeLog, BoxerMediaAdditional, BoxerIdentification
from biz import models, constants


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['nick_name', 'gender', 'address', 'name', 'nation', 'birthday', 'height', 'weight', 'profession']


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H-%M-%S')
    user_basic_info = serializers.SerializerMethodField()

    @staticmethod
    def get_user_basic_info(instance):
        if hasattr(instance, 'user_profile'):
            return UserProfileSerializer(instance.user_profile).data

    class Meta:
        model = models.User
        fields = ['id', 'username', 'mobile', 'date_joined', 'user_basic_info']


class CoinMoneyBaseSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format('%Y-%m-%d %H:%M:%S'), required=False)

    def create(self, validated_data):
        model_class = self.Meta.model
        alias = validated_data.pop('alias')
        user = validated_data['user']
        change_amount = validated_data['change_amount']
        last_amount = getattr(user, '{}_balance'.format(alias))
        remain_amount = last_amount + change_amount
        operator = self.context['request'].user

        setattr(user, '{}_balance'.format(alias), remain_amount)
        user.save()

        change_log = model_class.objects.create(last_amount=last_amount,
                                                operator=operator,
                                                remain_amount=remain_amount,
                                                **validated_data)

        return change_log


class CoinLogSerializer(CoinMoneyBaseSerializer):
    change_type = serializers.ChoiceField(choices=constants.COIN_CHANGE_TYPE_CHOICES,
                                          error_messages={'invalid_choice': '拳豆修改类型未知'})

    def create(self, validated_data):
        validated_data['alias'] = 'coin'
        return super(CoinLogSerializer, self).create(validated_data)

    class Meta:
        model = CoinChangeLog
        fields = '__all__'


class MoneyLogSerializer(CoinMoneyBaseSerializer):
    change_type = serializers.ChoiceField(choices=constants.MONEY_CHANGE_TYPE_CHOICES,
                                          error_messages={'invalid_choice': '钱包余额修改类型未知'})

    def create(self, validated_data):
        validated_data['alias'] = 'money'
        return super(MoneyLogSerializer, self).create(validated_data)

    class Meta:
        model = MoneyChangeLog
        fields = '__all__'


class BoxerMediaAdditionalSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoxerMediaAdditional
        fields = ['media_url', 'media_type']


class BoxerIdentificationSerializer(serializers.ModelSerializer):
    boxer_identification_additional = BoxerMediaAdditionalSerializer(many=True)
    nick_name = serializers.SerializerMethodField()

    class Meta:
        model = BoxerIdentification
        fields = '__all__'
        read_only_fields = ('lock_state',)

    @staticmethod
    def get_nick_name(obj):
        has_profile = hasattr(obj.user, 'user_profile')
        return obj.user.user_profile.nick_name if has_profile else None
