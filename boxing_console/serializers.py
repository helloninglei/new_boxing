# -*- coding: utf-8 -*-
from django.db import transaction
from django.forms.models import model_to_dict
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from biz.models import CoinChangeLog, MoneyChangeLog, BoxerIdentification, Course, BoxingClub, HotVideo, PayOrder
from biz import models, constants, redis_client
from biz.validator import validate_mobile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['nick_name', 'gender', 'address', 'name', 'nation', 'birthday', 'height', 'weight', 'profession']


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H-%M-%S')
    user_basic_info = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()
    is_boxer = serializers.SerializerMethodField()
    boxer_id = serializers.CharField(source="boxer_identification.id")

    def get_is_boxer(self, instance):
        return BoxerIdentification.objects.filter(
            user=instance, authentication_state=constants.BOXER_AUTHENTICATION_STATE_APPROVED).exists()

    def get_share_count(self, instance):
        return 0  # todo 分享数

    def get_follower_count(self, instance):
        return redis_client.follower_count(instance.id)

    def get_following_count(self, instance):
        return redis_client.following_count(instance.id)

    def get_user_basic_info(self, instance):
        if hasattr(instance, 'user_profile'):
            return UserProfileSerializer(instance.user_profile).data

    class Meta:
        model = models.User
        fields = [
            "id", "mobile", "following_count", "follower_count", "share_count", "money_balance", "is_boxer",
            "user_basic_info", "date_joined", "boxer_id"
        ]


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
    allowed_course = serializers.ListField(child=serializers.CharField())

    def validate(self, attrs):
        if attrs.get('authentication_state') == constants.BOXER_AUTHENTICATION_STATE_REFUSE and \
                not attrs.get('refuse_reason'):
            raise ValidationError({'refuse_reason': ['驳回理由是必填项']})
        if attrs.get('authentication_state') == constants.BOXER_AUTHENTICATION_STATE_APPROVED:
            if not attrs.get('allowed_course'):
                raise ValidationError({'allowed_course': ['可开通的课程类型是必填项']})
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
    allowed_course = serializers.SerializerMethodField()
    boxer_id = serializers.SerializerMethodField()

    def get_boxer_name(self, instance):
        return instance.boxer.real_name

    def get_mobile(self, instance):
        return instance.boxer.mobile

    def get_is_professional_boxer(self, instance):
        return instance.boxer.is_professional_boxer

    def get_is_accept_order(self, instance):
        return not instance.boxer.is_locked

    def get_allowed_course(self, instance):
        return instance.boxer.allowed_course

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
    user_mobile = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    user_nickname = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    course_duration = serializers.SerializerMethodField()
    course_validity = serializers.SerializerMethodField()
    boxer_name = serializers.SerializerMethodField()
    boxer_mobile = serializers.SerializerMethodField()
    club_name = serializers.SerializerMethodField()

    def get_user_mobile(self, instance):
        return instance.user.mobile

    def get_user_id(self, instance):
        return instance.user.pk

    def get_user_nickname(self, instance):
        return instance.user.user_profile.nick_name

    def get_course_name(self, instance):
        return instance.content_object.course_name

    def get_course_duration(self, instance):
        return instance.content_object.duration

    def get_course_validity(self, instance):
        return instance.content_object.validity

    def get_boxer_name(self, instance):
        return instance.content_object.boxer.real_name

    def get_boxer_mobile(self, instance):
        return instance.content_object.boxer.mobile

    def get_club_name(self, instance):
        return instance.content_object.club.name

    class Meta:
        model = PayOrder
        fields = ("id", "status", "out_trade_no", "payment_type", "amount", "order_time", "pay_time",
                  "course_name", "course_duration", "course_validity", "user_mobile", "user_id", "user_nickname",
                  "boxer_name", "boxer_mobile", "object_id", "club_name")


class NewsSerializer(serializers.ModelSerializer):
    operator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = serializers.SerializerMethodField()
    comment_count = serializers.IntegerField(read_only=True)

    def get_author(self, obj):
        if hasattr(obj.operator, 'user_profile'):
            return obj.operator.user_profile.nick_name
        return obj.operator.mobile

    class Meta:
        model = models.GameNews
        exclude = ('created_time', 'updated_time')
        read_only_fields = ('views_count',)


class AdminSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(validators=[validate_mobile])

    def validate(self, attrs):
        user = self.Meta.model.objects.filter(mobile=attrs['mobile']).first()
        if not user:
            raise ValidationError("该手机号未注册，请先在app注册！")
        if user and user.is_staff:
            raise ValidationError("该用户已是管理员，无需再添加！")
        return attrs

    def create(self, validated_data):
        user = self.Meta.model.objects.get(mobile=validated_data['mobile'])
        user.is_staff = True
        user.save()
        return user

    class Meta:
        model = models.User
        fields = ["id", 'mobile']


class ReportSerializer(serializers.ModelSerializer):
    reason = serializers.CharField(source='get_reason_display')
    reported_user = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        return model_to_dict(obj.content_object)

    def get_reported_user(self, obj):
        return obj.content_object.user.id

    def get_content_type(self, obj):
        return obj.content_object._meta.verbose_name

    class Meta:
        model = models.Report
        exclude = ('updated_time', 'operator')


class ReportHandleSerializer(serializers.ModelSerializer):
    operator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Report
        fields = ('id', 'operator')
