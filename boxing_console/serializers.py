# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from biz.models import CoinChangeLog, MoneyChangeLog, BoxerIdentification
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


class CoinMoneyBaseSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format('%Y-%m-%d %H:%M:%S'), required=False)
    operator = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        model_class = self.Meta.model
        alias = validated_data.pop('alias')
        user = validated_data['user']
        change_amount = validated_data['change_amount']
        last_amount = getattr(user, '{}_balance'.format(alias))
        remain_amount = last_amount + change_amount

        setattr(user, '{}_balance'.format(alias), remain_amount)
        user.save()

        change_log = model_class.objects.create(last_amount=last_amount,
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


class BoxerIdentificationSerializer(serializers.ModelSerializer):
    honor_certificate_images = serializers.ListField(child=serializers.URLField(), required=False)
    competition_video = serializers.URLField(required=False)
    nick_name = serializers.SerializerMethodField()
    allow_lesson = serializers.ListField(child=serializers.CharField())

    def validate(self, attrs):
        if attrs.get('authentication_state') == constants.BOXER_AUTHENTICATION_STATE_REFUSE and \
                not attrs.get('refuse_reason'):
            raise ValidationError({'refuse_reason': ['驳回理由是必填项']})
        if attrs.get('authentication_state') == constants.BOXER_AUTHENTICATION_STATE_APPROVED and \
                not attrs.get('allow_lesson'):
            raise ValidationError({'allow_lesson': ['可开通的课程类型是必填项']})
        return attrs

    class Meta:
        model = BoxerIdentification
        fields = '__all__'
        read_only_fields = ('user', 'real_name', 'height', 'weight', 'birthday', 'identity_number',
                            'mobile', 'is_professional_boxer', 'club', 'job', 'introduction', 'experience',
                            'honor_certificate_images', 'competition_video')

    def get_nick_name(self, obj):
        has_profile = hasattr(obj.user, 'user_profile')
        return obj.user.user_profile.nick_name if has_profile else None
