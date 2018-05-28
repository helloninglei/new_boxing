# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from django.conf import settings
from django.db import transaction
from django.core.validators import URLValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from biz.models import CoinChangeLog, MoneyChangeLog, BoxerIdentification, Course, BoxingClub, HotVideo, PayOrder, \
    Message, Comment
from biz import models, constants, redis_client
from biz.utils import get_model_class_by_name, get_video_cover_url
from biz.validator import validate_mobile
from biz.redis_client import get_number_of_share
from biz.constants import BANNER_LINK_TYPE_IN_APP_NATIVE, BANNER_LINK_MODEL_TYPE

url_validator = URLValidator()
datetime_format = settings.REST_FRAMEWORK['DATETIME_FORMAT']


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
        return get_number_of_share(instance.id)

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
    honor_certificate_images = serializers.ListField(child=serializers.CharField(), required=False)
    competition_video = serializers.CharField(required=False)
    nick_name = serializers.CharField(source='user.user_profile.nick_name', read_only=True)
    allowed_course = serializers.ListField(child=serializers.CharField())
    gender = serializers.BooleanField(source='user.user_profile.gender', read_only=True)

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


class CourseSerializer(serializers.ModelSerializer):
    boxer_name = serializers.CharField(source='boxer.real_name', read_only=True)
    mobile = serializers.CharField(source='boxer.mobile', read_only=True)
    is_professional_boxer = serializers.BooleanField(source='boxer.is_professional_boxer', read_only=True)
    is_accept_order = serializers.SerializerMethodField()
    allowed_course = serializers.ListField(source='boxer.allowed_course', read_only=True)
    boxer_id = serializers.IntegerField(source='boxer.pk', read_only=True)

    def get_is_accept_order(self, instance):
        return not instance.boxer.is_locked

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


class HotVideoShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotVideo
        fields = ('is_show',)


class CourseOrderSerializer(serializers.ModelSerializer):
    user_mobile = serializers.CharField(source='user.mobile', read_only=True)
    user_id = serializers.IntegerField(source='user.pk', read_only=True)
    user_nickname = serializers.CharField(source='user.user_profile.nick_name', read_only=True)
    course_name = serializers.CharField(source='content_object.course_name', read_only=True)
    course_duration = serializers.IntegerField(source='content_object.duration', read_only=True)
    course_price = serializers.IntegerField(source='content_object.price', read_only=True)
    course_validity = serializers.DateField(source='content_object.validity', read_only=True)
    boxer_id = serializers.IntegerField(source='content_object.boxer.pk', read_only=True)
    boxer_name = serializers.CharField(source='content_object.boxer.real_name', read_only=True)
    boxer_mobile = serializers.CharField(source='content_object.boxer.mobile', read_only=True)
    club_name = serializers.CharField(source='content_object.club.name', read_only=True)

    class Meta:
        model = PayOrder
        fields = ("id", "status", "out_trade_no", "payment_type", "amount", "order_time", "pay_time",
                  "course_name", "course_duration", "course_validity", "course_price", "user_mobile",
                  "user_id", "user_nickname", "boxer_name", "boxer_mobile", "object_id", "club_name",
                  'boxer_id')


class NewsSerializer(serializers.ModelSerializer):
    operator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = serializers.CharField(source='operator.user_profile.nick_name', read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        if attrs.get('push_news'):
            start_time = attrs.get('start_time').replace(tzinfo=None)
            end_time = attrs.get('end_time').replace(tzinfo=None)

            if start_time < datetime.now():
                raise ValidationError({'message': ['开始时间必须是以后的时间']})
            if start_time > datetime.now() + timedelta(days=7):
                raise ValidationError({'message': ['开始时间必须是七天内']})
            if end_time < start_time:
                raise ValidationError({'message': ['结束时间必须大于开始时间']})
            if end_time > start_time + timedelta(days=14):
                raise ValidationError({'message': ['结束时间必须在开始时间以后的14天内']})
        return attrs

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

    def get_content(self, instance):
        obj = instance.content_object
        user = obj.user
        created_time = obj.created_time
        if isinstance(obj, Message):
            content = obj.content
            pictures = obj.images[:]
            if obj.video:
                pictures.append(get_video_cover_url(obj.video))
        elif isinstance(obj, Comment):
            content = obj.content
            pictures = []
        else:
            content = obj.name
            pictures = [get_video_cover_url(obj.try_url)]
        return {
            'nick_name': user.user_profile.nick_name if hasattr(user, 'user_profile') else None,
            'created_time': created_time.strftime(datetime_format),
            'content': content,
            'pictures': pictures,
        }

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


class BannerSerializer(serializers.ModelSerializer):
    operator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        link = attrs.get('link')
        if attrs.get('link_type') == BANNER_LINK_TYPE_IN_APP_NATIVE:
            params = link.split(':')
            if len(params) != 2:
                raise ValidationError({'message': ['链接格式错误: model_name:obj_id']})
            model_name, obj_id = params
            if model_name not in BANNER_LINK_MODEL_TYPE:
                raise ValidationError({'message': ['未知的链接对象']})
            model_class = get_model_class_by_name(model_name)
            if not model_class.objects.filter(pk=obj_id).exists():
                raise ValidationError({'message': [f'{model_class._meta.verbose_name}:{obj_id} 不存在']})
        else:
            url_validator(link)
        return attrs

    class Meta:
        model = models.Banner
        exclude = ('created_time', 'updated_time')
