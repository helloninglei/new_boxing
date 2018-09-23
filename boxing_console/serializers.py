# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from django.utils import timezone
from distutils.version import StrictVersion
import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core.validators import URLValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from biz.models import User, CoinChangeLog, BoxerIdentification, Course, BoxingClub, HotVideo, Message, Comment, \
    OrderComment, AppVersion
from biz import models, constants, redis_client
from biz.services.money_balance_service import change_money
from biz.utils import get_model_class_by_name, hans_to_initial
from biz.validator import validate_mobile
from biz.redis_client import get_number_of_share, get_message_forward_count, get_hotvideo_forward_count
from biz.constants import BANNER_LINK_TYPE_IN_APP_NATIVE, BANNER_LINK_MODEL_TYPE, WITHDRAW_STATUS_WAITING, \
    WITHDRAW_STATUS_APPROVED, WITHDRAW_STATUS_REJECTED, MONEY_CHANGE_TYPE_INCREASE_REJECT_WITHDRAW_REBACK, \
    OFFICIAL_ACCOUNT_CHANGE_TYPE_WITHDRAW, PAYMENT_STATUS_UNPAID, MONEY_CHANGE_TYPE_INCREASE_OFFICIAL_RECHARGE, \
    USER_TYPE_MAP, MAX_HOT_VIDEO_BIND_USER_COUNT, HOT_VIDEO_USER_ID, APPVERSION_FUTURE, APPVERSION_NOW, ANDROID, IOS
from biz.services.official_account_service import create_official_account_change_log

url_validator = URLValidator()
datetime_format = settings.REST_FRAMEWORK['DATETIME_FORMAT']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['nick_name', 'gender', 'address', 'name', 'nation', 'birthday', 'height', 'weight', 'profession']


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField()
    user_basic_info = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()
    is_boxer = serializers.SerializerMethodField()
    boxer_id = serializers.CharField(source="boxer_identification.id")
    user_type = serializers.SerializerMethodField()

    def get_user_type(self, instance):
        return instance.get_user_type_display() or "普通用户"

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
            "user_basic_info", "date_joined", "boxer_id", "coin_balance", "user_type", "title"
        ]


class CoinBaseSerializer(serializers.ModelSerializer):
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


class CoinLogSerializer(CoinBaseSerializer):
    change_type = serializers.ChoiceField(choices=constants.COIN_CHANGE_TYPE_CHOICES,
                                          error_messages={'invalid_choice': '拳豆修改类型未知'})

    def create(self, validated_data):
        validated_data['alias'] = 'coin'
        return super(CoinLogSerializer, self).create(validated_data)

    class Meta:
        model = CoinChangeLog
        fields = '__all__'


class BoxerIdentificationSerializer(serializers.ModelSerializer):
    honor_certificate_images = serializers.ListField(child=serializers.CharField(), required=False)
    competition_video = serializers.CharField(required=False)
    nick_name = serializers.CharField(source='user.user_profile.nick_name', read_only=True)
    allowed_course = serializers.ListField(child=serializers.CharField())
    gender = serializers.BooleanField(source='user.user_profile.gender', read_only=True)
    mobile = serializers.CharField(source='user.mobile')
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return redis_client.get_user_title(instance.user) or instance.user.title

    def validate(self, attrs):
        attrs['is_locked'] = False
        return attrs

    class Meta:
        model = BoxerIdentification
        fields = '__all__'
        read_only_fields = ('user', 'real_name', 'height', 'weight', 'birthday', 'identity_number',
                            'mobile', 'is_professional_boxer', 'club', 'job', 'introduction', 'experience',
                            'honor_certificate_images', 'competition_video')


class BoxerApproveSerializer(serializers.Serializer):
    allowed_course = serializers.ListField()
    title = serializers.CharField(max_length=16)

    class Meta:
        fields = ('allowed_course', 'title')


class BoxerRefuseSerializer(serializers.Serializer):
    refuse_reason = serializers.CharField(max_length=100)

    class Meta:
        fields = ('refuse_reason',)


class CourseSerializer(serializers.ModelSerializer):
    boxer_name = serializers.CharField(source='boxer.real_name', read_only=True)
    mobile = serializers.CharField(source='boxer.user.mobile', read_only=True)
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
    avatar = serializers.CharField(max_length=128, required=True)
    province = serializers.CharField(max_length=10, required=False)
    city = serializers.CharField(max_length=10, required=False)
    address = serializers.CharField(max_length=30, required=True)

    def validate(self, attrs):
        longitude = attrs['longitude']
        latitude = attrs['latitude']
        attrs['province'], attrs['city'], _ = self.get_location_info(longitude, latitude)
        attrs['city_index_letter'] = hans_to_initial(attrs['city'])
        return attrs

    @transaction.atomic
    def save(self, **kwargs):
        instance = super().save(**kwargs)
        redis_client.record_object_location(instance, instance.longitude, instance.latitude)
        return instance

    @staticmethod
    def get_location_info(longitude, latitude):
        """
        http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding-abroad 百度api文档说明
        response data:
        {
            "status":0,
            "result":{
                "location":{
                    "lng":116.32899999999994,
                    "lat":39.93400007551505},
                "formatted_address":"北京市海淀区增光路35-6号",
                "addressComponent":{
                    "country":"中国",
                    "province":"北京市",
                    "city":"北京市",
                    "district":"海淀区",,
                    "street":"增光路",,
                    "distance":"13"}}
        }
        """
        url = settings.BAIDU_MAP_URL
        params = {'location': f'{latitude},{longitude}',
                  'ak': settings.BAIDU_MAP_AK,
                  'output': 'json'
                  }
        res = requests.get(url=url, params=params)
        json_res = res.json()
        result = json_res.get('result')
        address = result.get('formatted_address')
        location_detail = result.get('addressComponent')
        province = location_detail.get('province')
        city = location_detail.get('city')
        return province, city, address

    class Meta:
        model = BoxingClub
        fields = '__all__'


class HotVideoUserSerializer(serializers.ModelSerializer):
    nick_name = serializers.CharField(source='user_profile.nick_name')
    avatar = serializers.CharField(source='user_profile.avatar')

    class Meta:
        model = User
        fields = ('id', 'nick_name', 'avatar')


class HotVideoSerializer(serializers.ModelSerializer):
    operator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    sales_count = serializers.IntegerField(read_only=True)
    price_amount = serializers.IntegerField(read_only=True)
    user_list = serializers.SerializerMethodField()
    users = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    push_to_hotvideo = serializers.BooleanField(default=False, write_only=True)  # 绑定热门视频用户
    tag_name = serializers.CharField(source='get_tag_display', read_only=True)
    forward_count = serializers.SerializerMethodField()
    tag = serializers.ChoiceField(choices=constants.HOT_VIDEO_TAG_CHOICES, allow_blank=False)

    def get_forward_count(self, instance):
        return get_hotvideo_forward_count(instance.id)

    def get_user_list(self, instance):
        return HotVideoUserSerializer(instance.users, many=True).data

    def validate(self, attrs):
        if len(attrs['users']) > MAX_HOT_VIDEO_BIND_USER_COUNT:
            raise ValidationError({'message': [f'最多关联{MAX_HOT_VIDEO_BIND_USER_COUNT}个用户']})
        if not User.objects.filter(id__in=attrs['users']).exists():
            raise ValidationError({'message': ['用户不存在']})
        if attrs.pop('push_to_hotvideo'):
            attrs['users'].append(HOT_VIDEO_USER_ID)

        if attrs.get('push_hot_video'):
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
        model = HotVideo
        fields = ('id', 'name', 'description', 'sales_count', 'price_amount', 'url', 'try_url', 'price',
                  'operator', 'is_show', 'created_time', 'cover', 'stay_top', 'tag', 'tag_name', 'users', 'user_list',
                  'push_to_hotvideo', 'push_hot_video', 'start_time', 'end_time', 'like_count', 'forward_count',
                  'views_count')


class HotVideoShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotVideo
        fields = ('is_show',)


class CourseOrderSerializer(serializers.ModelSerializer):
    user_mobile = serializers.CharField(source='user.mobile', read_only=True)
    user_id = serializers.IntegerField(source='user.pk', read_only=True)
    user_nickname = serializers.CharField(source='user.user_profile.nick_name', read_only=True)
    boxer_id = serializers.IntegerField(source='boxer.pk', read_only=True)
    boxer_name = serializers.CharField(source='boxer.real_name', read_only=True)
    boxer_mobile = serializers.CharField(source='boxer.user.mobile', read_only=True)
    club_name = serializers.CharField(source='club.name', read_only=True)
    out_trade_no = serializers.IntegerField(source='pay_order.out_trade_no', read_only=True)
    payment_type = serializers.IntegerField(source='pay_order.payment_type', read_only=True)
    comment_score = serializers.SerializerMethodField()
    comment_time = serializers.SerializerMethodField()
    comment_content = serializers.SerializerMethodField()
    comment_images = serializers.SerializerMethodField()

    def get_comment_score(self, instance):
        comment = self.get_comment(instance)
        return comment.score if comment else None

    def get_comment_time(self, instance):
        comment = self.get_comment(instance)
        return timezone.localtime(comment.created_time).strftime(datetime_format) if comment else None

    def get_comment_content(self, instance):
        comment = self.get_comment(instance)
        return comment.content if comment else None

    def get_comment_images(self, instance):
        comment = self.get_comment(instance)
        return comment.images if comment else None

    @staticmethod
    def get_comment(instance):
        try:
            comment = OrderComment.objects.get(order=instance)
            return comment
        except ObjectDoesNotExist:
            return None

    class Meta:
        model = models.CourseOrder
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    operator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = serializers.CharField(source='operator.user_profile.nick_name', read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    pub_time = serializers.DateTimeField(source='updated_time', read_only=True)

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
    status = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    operator = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()

    def get_content_type(selfs, instance):
        if instance.content_object:
            return instance.content_object._meta.verbose_name

    def _get_reported_user(self, instance):
        obj = instance.content_object
        if obj:
            if not isinstance(obj, HotVideo):
                return obj.user
            return obj.users.first()

    def get_reported_user(self, instance):
        return self._get_reported_user(instance).id

    def get_operator(self, instance):
        return instance.operator.user_profile.nick_name if instance.operator and instance.operator.user_profile else None

    def get_status(self, instance):
        if instance.status == 1:
            return '未处理'
        return '已处理'

    def get_result(self, instance):
        if instance.status > 1:
            return instance.get_status_display()

    def get_content(self, instance):
        obj = instance.content_object
        if not obj:
            return {}
        user = self._get_reported_user(instance)
        created_time = obj.created_time
        video = None
        pictures = []

        if isinstance(obj, Message):
            content = obj.content
            pictures = obj.images
            video = obj.video
        elif isinstance(obj, Comment):
            content = obj.content
        else:
            content = obj.name
            video = obj.url
        return {
            'nick_name': user.user_profile.nick_name if hasattr(user, 'user_profile') else None,
            'created_time': created_time.strftime(datetime_format),
            'content': content,
            'pictures': pictures,
            'video': video,
        }

    class Meta:
        model = models.Report
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    operator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        pk = self.context['view'].kwargs.get('pk')
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
        if models.Banner.objects.filter(order_number=attrs.get('order_number')).exclude(id=pk).exists():
            raise ValidationError({'message': ['序号已存在']})
        return attrs

    class Meta:
        model = models.Banner
        exclude = ('created_time', 'updated_time')


class CourseSettleOrderSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id')
    course_name = serializers.CharField(source='course.get_course_name_display')
    boxer_name = serializers.CharField(source='course.boxer.real_name')
    boxer_mobile = serializers.CharField(source='course.boxer.user.mobile')
    course_amount = serializers.IntegerField(source='course_order.course_price')
    buyer_mobile = serializers.CharField(source='order.user.mobile')
    predicted_settle_date = serializers.SerializerMethodField()
    actual_settle_date = serializers.DateField(source='settled_date', format='%Y%m%d')

    def get_predicted_settle_date(self, attrs):
        return (attrs.created_time + timedelta(days=7)).strftime('%Y%m%d')

    class Meta:
        model = models.CourseSettleOrder
        exclude = ('order', 'course', 'created_time')


class WithdrawLogSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="user.id", read_only=True)
    user_nickname = serializers.CharField(source="user.user_profile.nick_name", read_only=True)
    user_mobile = serializers.CharField(source="user.mobile", read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    def validate(self, attrs):
        if self.instance.status != WITHDRAW_STATUS_WAITING:
            raise ValidationError("该条记录已经审核过了，不能重复审核！")
        if self.context['operate_type'] == "approved":
            attrs['status'] = WITHDRAW_STATUS_APPROVED
        if self.context['operate_type'] == "rejected":
            attrs['status'] = WITHDRAW_STATUS_REJECTED
        attrs['operator'] = self.context['request'].user
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if instance.status == WITHDRAW_STATUS_REJECTED:
            change_money(instance.user, instance.amount, change_type=MONEY_CHANGE_TYPE_INCREASE_REJECT_WITHDRAW_REBACK,
                         remarks=instance.order_number)
        if instance.status == WITHDRAW_STATUS_APPROVED:
            create_official_account_change_log(
                -instance.amount, self.context['request'].user,
                change_type=OFFICIAL_ACCOUNT_CHANGE_TYPE_WITHDRAW, remarks=instance.order_number
            )
        return instance

    class Meta:
        model = models.WithdrawLog
        fields = ["id", "order_number", "user_id", "user_nickname", "user_mobile", "created_time", "amount",
                  "withdraw_account", "status"]
        read_only_fields = ("order_number", "created_time", "amount", "withdraw_account")


class MoneyBalanceChangeLogSerializer(serializers.ModelSerializer):
    change_type = serializers.CharField(source="get_change_type_display")
    remarks = serializers.SerializerMethodField()
    change_amount = serializers.SerializerMethodField()

    def get_change_amount(self, instance):
        return "+" + str(instance.change_amount) if instance.change_amount > 0 else str(instance.change_amount)

    def get_remarks(self, instance):
        if instance.change_type == MONEY_CHANGE_TYPE_INCREASE_OFFICIAL_RECHARGE:
            return instance.operator.mobile
        return instance.remarks

    class Meta:
        model = models.MoneyChangeLog
        fields = ["change_amount", "created_time", "remarks", "change_type"]


class PayOrdersReadOnlySerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source="user.user_profile.nick_name")
    user_mobile = serializers.CharField(source="user.mobile")
    device = serializers.CharField(source="get_device_display")
    payment_type = serializers.CharField(source="get_payment_type_display")
    remarks = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_status(self, instance):
        if instance.status == PAYMENT_STATUS_UNPAID:
            return "支付未完成"
        return "支付成功"

    def get_remarks(self, instance):
        return f"【{instance.content_object.__class__._meta.verbose_name}】id:{instance.content_object.id}"

    class Meta:
        model = models.PayOrder
        exclude = ['finish_time', "object_id", "pay_time", "content_type"]


class OfficialAccountChangeLogsSerializer(serializers.ModelSerializer):
    change_type = serializers.CharField(source="get_change_type_display")

    class Meta:
        model = models.OfficialAccountChangeLog
        fields = ["id", "change_amount", "created_time", "remarks", "change_type"]


class CourseOrderInsuranceSerializer(serializers.Serializer):
    insurance_amount = serializers.IntegerField(min_value=0)

    def validate(self, attrs):
        if self.context['order'].status != constants.COURSE_PAYMENT_STATUS_WAIT_USE:
            raise ValidationError("订单不是待使用状态，不能标记保险")
        if attrs['insurance_amount'] > self.context['order'].amount:
            raise ValidationError("保险金额不能超过订单金额")
        if attrs['insurance_amount'] < 0:
            raise ValidationError("保险金额不能为负值")
        return attrs

    class Meta:
        fields = ('insurance_amount',)


class MessageSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    avatar = serializers.CharField(source='user.user_profile.avatar')
    forward_count = serializers.SerializerMethodField()
    images = serializers.ListField(child=serializers.CharField(max_length=200), required=False)
    nick_name = serializers.CharField(source='user.user_profile.nick_name')
    user_type = serializers.SerializerMethodField()
    mobile = serializers.CharField(source='user.mobile')

    def get_user_type(self, instance):
        return instance.user.get_user_type_display() or '普通用户'

    def get_forward_count(self, instance):
        return get_message_forward_count(instance.id)

    class Meta:
        model = models.Message
        exclude = ('is_deleted', 'user', 'updated_time')
        read_only_fields = ('content', 'images', 'video', 'is_deleted', 'created_time')


class EditUserInfoSerializer(serializers.ModelSerializer):
    change_amount = serializers.IntegerField(write_only=True, min_value=0)
    user_type = serializers.CharField(source="get_user_type_display")

    def validate(self, attrs):
        attrs['user_type'] = dict(zip(USER_TYPE_MAP.values(), USER_TYPE_MAP.keys())).get(attrs['get_user_type_display'])
        attrs['money_balance'] = self.instance.money_balance + attrs['change_amount']
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        models.MoneyChangeLog.objects.create(user=instance, change_type=MONEY_CHANGE_TYPE_INCREASE_OFFICIAL_RECHARGE,
                                             last_amount=instance.money_balance,
                                             change_amount=validated_data['change_amount'],
                                             remain_amount=validated_data['money_balance'],
                                             operator=self.context['request'].user)
        return super(EditUserInfoSerializer, self).update(instance, validated_data)

    class Meta:
        model = models.User
        fields = ('title', "user_type", "money_balance", "change_amount")
        read_only_fields = ("money_balance",)


class WordFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WordFilter
        fields = ['id', "sensitive_word"]


class AppVersionSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['status'] != APPVERSION_FUTURE:
            raise ValidationError(detail='只允许未发布版本')

        try:
            StrictVersion(attrs['version'])
        except ValueError:
            raise ValidationError(detail={'detail': '版本号格式错误 eg: x.y.z'})

        if attrs['platform'] == ANDROID:
            if not attrs['package']:
                raise ValidationError(detail={'detail': '软件包地址不能为空'})
            current = AppVersion.objects.get(status=APPVERSION_NOW, platform=ANDROID)
            if StrictVersion(attrs['version']) <= StrictVersion(current.version):
                raise ValidationError(detail={'detail': '发布版本号不得低于当前版本'})
            if not attrs['inner_number']:
                raise ValidationError(detail={'detail': '内部版本号不得为空'})
            if not isinstance(attrs['inner_number'], int):
                raise ValidationError(detail={'detail': '内部版本号类型错误'})
            if attrs['inner_number'] <= current.inner_number:
                raise ValidationError(detail={'detail': '内部版本号不得低于当前内部版本号'})

        if attrs['platform'] == IOS:
            current = AppVersion.objects.get(status=APPVERSION_NOW, platform=IOS)
            if StrictVersion(attrs['version']) <= StrictVersion(current.version):
                raise ValidationError(detail={'detail': '发布版本号不得低于当前版本'})
            attrs['inner_number'] = 0
            attrs['package'] = ''

        return attrs

    class Meta:
        model = models.AppVersion
        exclude = ('operator', 'created_time')
