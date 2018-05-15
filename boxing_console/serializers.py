# -*- coding: utf-8 -*-
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from biz.models import CoinChangeLog, MoneyChangeLog, BoxerIdentification, Course, BoxingClub, HotVideo, PayOrder
from biz import models, constants, redis_client



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
    allowed_lessons = serializers.ListField(child=serializers.CharField())

    def validate(self, attrs):
        if attrs.get('authentication_state') == constants.BOXER_AUTHENTICATION_STATE_REFUSE and \
                not attrs.get('refuse_reason'):
            raise ValidationError({'refuse_reason': ['驳回理由是必填项']})
        if attrs.get('authentication_state') == constants.BOXER_AUTHENTICATION_STATE_APPROVED:
            if not attrs.get('allowed_lessons'):
                raise ValidationError({'allowed_lessons': ['可开通的课程类型是必填项']})
            else:
                attrs['is_locked'] = False
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


class CourseSerializer(serializers.ModelSerializer):
    boxer_name = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    is_professional_boxer = serializers.SerializerMethodField()
    is_accept_order = serializers.SerializerMethodField()
    club = serializers.SerializerMethodField()
    allowed_lessons = serializers.SerializerMethodField()
    boxer_id = serializers.SerializerMethodField()

    def get_boxer_name(self, instance):
        return instance.boxer.real_name

    def get_mobile(self, instance):
        return instance.boxer.mobile

    def get_is_professional_boxer(self, instance):
        return instance.boxer.is_professional_boxer

    def get_is_accept_order(self, instance):
        return not instance.boxer.is_locked

    def get_club(self, instance):
        return instance.boxer.club

    def get_allowed_lessons(self, instance):
        return instance.boxer.allowed_lessons

    def get_boxer_id(self, instance):
        return instance.boxer.pk

    class Meta:
        model = Course
        exclude = ('boxer',)


class BoxingClubSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.CharField(), required=False)

    @transaction.atomic
    def save(self, **kwargs):
        instance = super().save(**kwargs)
        redis_client.record_boxing_club_location(instance)
        return instance

    class Meta:
        model = BoxingClub
        fields = '__all__'


class HotVideoSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    operator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    sales_count = serializers.IntegerField(read_only=True)
    price_amount = serializers.IntegerField(read_only=True)

    def validate(self, data):
        user_id = data['user_id']
        if not models.User.objects.filter(pk=user_id).exists():
            raise ValidationError({'user_id': [f'用户 {user_id} 不存在']})
        return data

    class Meta:
        model = HotVideo
        fields = ('id', 'user_id', 'name', 'description', 'sales_count', 'price_amount', 'url', 'try_url', 'price',
                  'operator', 'is_show', 'created_time')


class CourseOrderSerializer(serializers.ModelSerializer):


    class Meta:
        model = PayOrder
        fields = "__all__"