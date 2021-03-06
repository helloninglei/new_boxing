# -*- coding: utf-8 -*-
import re
from datetime import datetime

from django.db.models import Q
from django.forms import model_to_dict
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.compat import authenticate
from biz.constants import BOXER_AUTHENTICATION_STATE_WAITING, HOT_VIDEO_USER_ID, PAYMENT_TYPE, REPORT_OTHER_REASON, \
    PAYMENT_STATUS_PAID, SCHEDULE_STATUS_PUBLISHED
from biz.models import OrderComment, BoxingClub, User, Course, Match, Player
from biz.redis_client import follower_count, following_count, get_user_title, is_liking_hot_video
from biz.constants import MESSAGE_TYPE_ONLY_TEXT, MESSAGE_TYPE_HAS_IMAGE, MESSAGE_TYPE_HAS_VIDEO, \
    MONEY_CHANGE_TYPE_REDUCE_WITHDRAW
from biz.redis_client import is_following, get_object_location, set_user_title
from biz import models, constants
from biz.services.url_service import get_cdn_url
from biz.validator import validate_mobile, validate_password, validate_mobile_or_email
from biz.services.captcha_service import check_captcha
from biz import redis_const
from biz.redis_client import redis_client, get_message_forward_count, get_hotvideo_forward_count
from biz.redis_const import SENDING_VERIFY_CODE
from boxing_app.services import verify_code_service
from biz.utils import get_client_ip, get_device_platform, get_model_class_by_name, hans_to_initial
from biz.constants import WITHDRAW_MIN_CONFINE, DEFAULT_NICKNAME_FORMAT, DEFAULT_AVATAR
from biz.services.money_balance_service import change_money
from boxing_app.services.video_info_service import video_resolution

datetime_format = settings.REST_FRAMEWORK['DATETIME_FORMAT']
message_dateformat = '%Y-%m-%d %H:%M'

CDN_BASE_URL = settings.CDN_BASE_URL


class BoxerIdentificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    honor_certificate_images = serializers.ListField(child=serializers.CharField(), required=False)
    competition_video = serializers.CharField(required=False)
    allowed_course = serializers.ListField(child=serializers.CharField(), required=False)
    gender = serializers.BooleanField(source="user.user_profile.gender", read_only=True)
    avatar = serializers.SerializerMethodField()
    course_order_count = serializers.SerializerMethodField()
    title = serializers.CharField(max_length=16, write_only=True)
    user_type = serializers.CharField(source="user.get_user_type_display", read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['title'] = get_user_title(instance.user) or instance.user.title
        return ret

    def get_avatar(self, instance):
        return instance.user.user_profile.avatar and get_cdn_url(instance.user.user_profile.avatar)

    def get_course_order_count(self, instance):
        return instance.boxer_course_order.filter(status__gt=constants.COURSE_PAYMENT_STATUS_UNPAID).count()

    @atomic
    def update(self, instance, validated_data):
        validated_data['authentication_state'] = BOXER_AUTHENTICATION_STATE_WAITING
        validated_data['is_accept_order'] = False
        Course.objects.filter(boxer=instance).update(is_open=False)
        return super().update(instance, validated_data)

    def save(self, **kwargs):
        user = self.context['request'].user
        title = self.validated_data.pop('title')
        set_user_title(user, title)
        return super().save(**kwargs)

    class Meta:
        model = models.BoxerIdentification
        fields = '__all__'
        read_only_fields = ('authentication_state', 'is_locked')


class NearbyBoxerIdentificationSerializer(serializers.ModelSerializer):
    longitude = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    course_min_price = serializers.IntegerField(source='min_price')
    gender = serializers.BooleanField(source='user.user_profile.gender', read_only=True)
    avatar = serializers.SerializerMethodField()
    allowed_course = serializers.ListField(read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    city = serializers.SerializerMethodField()
    order_count = serializers.IntegerField()
    title = serializers.CharField(source='user.title')
    user_type = serializers.CharField(source="user.get_user_type_display", read_only=True)

    def get_avatar(self, instance):
        return instance.user.user_profile.avatar and get_cdn_url(instance.user.user_profile.avatar)

    def get_longitude(self, instance):
        club = self.get_boxer_club(instance)
        return club.longitude

    def get_latitude(self, instance):
        club = self.get_boxer_club(instance)
        return club.latitude

    def get_city(self, instance):
        club = self.get_boxer_club(instance)
        return club.city

    @staticmethod
    def get_boxer_loacation(obj):
        return get_object_location(obj)[0]

    @staticmethod
    def get_boxer_club(boxer):
        course = Course.objects.filter(boxer=boxer, is_open=True).last()
        return course.club

    class Meta:
        model = models.BoxerIdentification
        fields = ['id', 'longitude', 'latitude', 'course_min_price', 'order_count', 'gender', 'avatar', 'real_name',
                  'allowed_course', 'city', 'user_id', 'title', 'user_type']
        read_only_fields = ['boxer_id', 'longitude', 'latitude', 'course_min_price', 'order_count', 'gender', 'avatar',
                            'real_name', 'allowed_course', 'city', 'title']


def serialize_user(user, context):
    profile = user.user_profile

    return {
        'id': user.id,
        'identity': user.identity,
        'is_following': bool(is_following(context['request'].user.id, user.id)),
        'nick_name': profile.nick_name or DEFAULT_NICKNAME_FORMAT.format(user.id),
        'avatar': get_cdn_url(profile.avatar) if profile.avatar else None,
        "user_type": user.get_user_type_display()
    }


class DiscoverUserField(serializers.RelatedField):
    def to_representation(self, user):
        return serialize_user(user, self.context)


class MessageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.CharField(max_length=200), required=False)
    video = serializers.CharField(max_length=200, required=False)
    user = DiscoverUserField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    is_like = serializers.BooleanField(read_only=True)
    msg_type = serializers.SerializerMethodField()
    forward_count = serializers.SerializerMethodField()
    created_time = serializers.DateTimeField(format=message_dateformat, read_only=True)

    def get_forward_count(self, instance):
        return get_message_forward_count(instance.id) + instance.initial_forward_count

    def get_msg_type(self, obj):
        if obj.video:
            return MESSAGE_TYPE_HAS_VIDEO
        if obj.images:
            return MESSAGE_TYPE_HAS_IMAGE
        return MESSAGE_TYPE_ONLY_TEXT

    def validate(self, data):
        if data.get('video') and data.get('images'):
            raise ValidationError({'video': ['?????????????????????????????????']})
        if not data.get('content') and not data.get('images') and not data.get('video'):
            raise ValidationError({'message': ['????????????????????????????????????????????????']})
        return data

    def to_representation(self, instance: models.Message) -> dict:
        ret = super().to_representation(instance)
        ret.update(video_resolution(instance.video))
        return ret

    class Meta:
        model = models.Message
        fields = ['id', 'content', 'images', 'video', 'msg_type', 'created_time', 'user', 'like_count', 'comment_count',
                  'forward_count', 'is_like']


class MessageReadOnlySerializer(MessageSerializer):
    images = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    def get_images(self, instance):
        return [f"{CDN_BASE_URL}{image}" for image in instance.images]

    def get_video(self, instance):
        return instance.video and f"{CDN_BASE_URL}{instance.video}"


class BasicReplySerializer(serializers.ModelSerializer):
    user = DiscoverUserField(read_only=True)
    to_user = DiscoverUserField(read_only=True)

    class Meta:
        model = models.Comment
        fields = ['id', 'content', 'user', 'to_user', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    user = DiscoverUserField(read_only=True)
    replies = serializers.SerializerMethodField()

    def get_replies(self, obj):
        latest = obj.reply_list()
        return {
            'count': latest.count(),
            'results': BasicReplySerializer(latest, many=True, context=self.context).data
        }

    class Meta:
        model = models.Comment
        fields = ['id', 'content', 'user', 'replies', 'created_time']
        read_only_fields = ('created_time',)


class CommentMeMessageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.CharField(max_length=200), required=False)
    user = serializers.SerializerMethodField()

    def get_user(self, instance):
        user = instance.user
        profile = user.user_profile
        return {
            'id': user.id,
            'identity': user.identity,
            'nick_name': profile.nick_name or DEFAULT_NICKNAME_FORMAT.format(user.id),
            'avatar': get_cdn_url(profile.avatar) if profile.avatar else None,
            "user_type": user.get_user_type_display()
        }

    class Meta:
        model = models.Message
        fields = ['id', 'content', 'images', 'video', 'created_time', 'user']


class CommentMeHotVideoSerializer(serializers.ModelSerializer):
    is_paid = serializers.SerializerMethodField()

    def get_is_paid(self, instance):
        return instance.orders.filter(status=PAYMENT_STATUS_PAID, user_id=self.context['request'].user).exists()

    class Meta:
        model = models.HotVideo
        fields = ('id', 'name', 'description', 'url', 'try_url', 'price', 'created_time', 'cover', 'is_paid')


class CommentMeNewsSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        return obj.picture and get_cdn_url(obj.picture)

    class Meta:
        model = models.GameNews
        fields = ('id', 'title', 'sub_title', 'picture', 'share_content')


class CommentMeSerializer(serializers.ModelSerializer):
    content = serializers.CharField(read_only=True)
    user = DiscoverUserField(read_only=True)
    to_object = serializers.SerializerMethodField()
    obj_type = serializers.SerializerMethodField()
    reply_or_comment = serializers.SerializerMethodField()

    def get_to_object(self, instance):
        serializer_choice = {"??????": CommentMeMessageSerializer,
                             "????????????": CommentMeHotVideoSerializer,
                             "????????????": CommentMeNewsSerializer}
        serializer = serializer_choice.get(instance.content_type.name)
        return serializer(instance.content_object, context=self.context).data

    def get_obj_type(self, instance):
        return instance.content_type.name

    def get_reply_or_comment(self, instance):
        return 'reply' if instance.parent else 'comment'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['created_time'] = instance.created_time.strftime('%Y-%m-%d %H:%M')
        return ret

    class Meta:
        model = models.Comment
        fields = ['content', 'user', 'obj_type', 'to_object', 'object_id', 'created_time', 'reply_or_comment']


class LikeSerializer(serializers.ModelSerializer):
    user = DiscoverUserField(read_only=True)
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = models.Like
        fields = ['user', 'created_time']


class LikeMeListSerializer(LikeSerializer):
    message = serializers.SerializerMethodField()

    def get_message(self, instance):
        user_serializer = type('UserSerializer', (DiscoverUserField,), {'context': self.context})(
            queryset=User.objects.all())
        message_user = user_serializer.to_representation(instance.message.user)
        get_fields = ['id', 'user', 'content', 'images', 'video', 'created_time']
        message_dict = model_to_dict(instance.message, fields=get_fields)
        message_dict.update(user=message_user)
        return message_dict

    class Meta:
        model = models.Like
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['reason'] != REPORT_OTHER_REASON:
            data['remark'] = None
        else:
            if not data.get('remark'):
                raise ValidationError({'remark': ['????????????????????????']})
        return data

    class Meta:
        model = models.Report
        fields = ['id', 'object_id', 'reason', 'remark']


class FollowUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    avatar = serializers.SerializerMethodField()
    nick_name = serializers.CharField(source='user_profile.nick_name')
    address = serializers.CharField(source='user_profile.address')
    bio = serializers.CharField(source='user_profile.bio')
    gender = serializers.BooleanField(source='user_profile.gender')
    identity = serializers.CharField()
    is_following = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()

    def get_avatar(self, user):
        return user.user_profile.avatar and get_cdn_url(user.user_profile.avatar)

    def get_user_type(self, user):
        return user.get_user_type_display()

    def get_is_following(self, user):
        current_user_id = self.context['current_user_id']
        return bool(is_following(current_user_id, user.id))

    class Meta:
        fields = ['id', 'gender', 'avatar', 'nick_name', 'address', 'bio', 'is_follow', 'identity', "user_type"]
        read_only_fields = '__all__'


class SendVerifyCodeSerializer(serializers.Serializer):
    mobile = serializers.CharField(validators=[validate_mobile])
    captcha = serializers.JSONField(required=False)

    def validate(self, attrs):
        if "captcha" in attrs:
            captcha = attrs['captcha']
            if not check_captcha(captcha.get("captcha_code"), captcha.get("captcha_hash")):
                raise ValidationError({"message": "????????????????????????"})
        else:
            if redis_client.exists(SENDING_VERIFY_CODE.format(mobile=attrs['mobile'])):
                raise ValidationError({"message": "????????????????????????"})
        return attrs


class RegisterSerializer(serializers.Serializer):
    mobile = serializers.CharField(validators=[validate_mobile])
    password = serializers.CharField(validators=[validate_password])
    verify_code = serializers.CharField()
    wechat_openid = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    weibo_openid = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate(self, attrs):
        wechat_openid, weibo_openid, mobile = attrs.get('wechat_openid'), attrs.get('weibo_openid'), attrs['mobile']
        if wechat_openid and weibo_openid:
            raise ValidationError("?????????????????????????????????????????????!")
        if User.objects.filter(mobile=attrs['mobile']).exists():
            raise ValidationError({"message": "?????????????????????"})
        if not verify_code_service.check_verify_code(mobile=mobile, verify_code=attrs['verify_code']):
            raise ValidationError({"message": "????????????????????????"})
        return attrs


class RegisterWithInfoSerializer(serializers.Serializer):
    avatar = serializers.CharField()
    gender = serializers.BooleanField()
    nick_name = serializers.CharField()
    mobile = serializers.CharField(validators=[validate_mobile])

    def validate(self, attrs):
        if not redis_client.exists(redis_const.REGISTER_INFO.format(mobile=attrs['mobile'])):
            raise ValidationError({"message": "????????????????????????????????????????????????"})
        if User.objects.filter(mobile=attrs['mobile']).exists():
            raise ValidationError("?????????????????????????????????!")
        return attrs


class HotVideoSerializer(serializers.ModelSerializer):
    is_paid = serializers.BooleanField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    url = serializers.SerializerMethodField()
    forward_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()
    try_url = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    bind_user = serializers.SerializerMethodField()
    other_users = serializers.SerializerMethodField()

    def _filter_users(self, instance):
        user_id = self.context['view'].kwargs.get('user_id')
        all_users = instance.users.all()
        # ?????????????????????????????????????????????????????????????????????
        if len(all_users) > 1:
            all_users = [user for user in all_users if user.id != HOT_VIDEO_USER_ID]

        # ?????????????????????????????????????????????????????????
        if user_id:
            all_users = sorted(all_users, key=lambda u: u.id != user_id)

        return all_users

    def get_bind_user(self, instance):
        user = self._filter_users(instance)[0]
        return serialize_user(user, self.context)

    def get_other_users(self, instance):
        users = self._filter_users(instance)[1:]
        return [serialize_user(user, self.context) for user in users]

    def get_is_like(self, instance):
        return is_liking_hot_video(self.context['request'].user.id, instance.id)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['is_hot'] = instance.operator.id == constants.HOT_VIDEO_USER_ID
        ret.update(video_resolution(instance.url))
        return ret

    def get_forward_count(self, instance):
        return get_hotvideo_forward_count(instance.id) + instance.initial_forward_count

    def get_views_count(self, instance):
        return instance.views_count + instance.initial_views_count

    def get_like_count(self, instance):
        return instance.like_count + instance.initial_like_count

    def get_url(self, instance):
        if instance.is_paid or instance.price == 0:
            return f'{CDN_BASE_URL}{instance.url}'

    def get_try_url(self, instance):
        return f'{CDN_BASE_URL}{instance.try_url}'

    class Meta:
        model = models.HotVideo
        fields = ('id', 'name', 'description', 'is_paid', 'comment_count', 'url', 'try_url', 'price', 'created_time',
                  'cover', 'views_count', 'like_count', 'forward_count', 'is_like', 'bind_user', 'other_users',
                  'push_hot_video',)


class HotVideoDetailSerializer(HotVideoSerializer):
    recommend_videos = serializers.SerializerMethodField()

    def get_recommend_videos(self, instance):
        return [{'id': v.id, 'name': v.name, 'url': v.url, 'user_id': v.users.first().id, 'price': v.price,
                 'cover': v.cover} for v in
                models.HotVideo.objects.filter(Q(tag=instance.tag) & Q(is_show=True) & ~Q(id=instance.id))[:5]]

    class Meta:
        model = models.HotVideo
        fields = ('id', 'name', 'description', 'is_paid', 'comment_count', 'url', 'try_url', 'price', 'created_time',
                  'cover', 'views_count', 'like_count', 'forward_count', 'is_like', 'bind_user', 'other_users',
                  'push_hot_video', 'recommend_videos')


class LoginIsNeedCaptchaSerializer(serializers.Serializer):
    mobile = serializers.CharField(validators=[validate_mobile])


class PaySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    device = serializers.SerializerMethodField()
    ip = serializers.SerializerMethodField()
    payment_type = serializers.ChoiceField(choices=PAYMENT_TYPE, required=False)
    content_object = serializers.SerializerMethodField()

    def get_content_object(self, obj):
        object_class = get_model_class_by_name(self.context['object_type'])
        return object_class.objects.get(pk=obj['id'])

    def get_ip(self, obj):
        return get_client_ip(self.context['request'])

    def get_device(self, obj):
        return get_device_platform(self.context['request'])


class BindAlipayAccountSerializer(serializers.Serializer):
    verify_code = serializers.CharField()
    alipay_account = serializers.CharField(validators=[validate_mobile_or_email])

    def validate(self, attrs):
        if not verify_code_service.check_verify_code(self.context['user'].mobile, attrs['verify_code']):
            raise ValidationError({"message": "????????????????????????"})
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(validators=[validate_password])
    mobile = serializers.CharField(validators=[validate_mobile])
    verify_code = serializers.CharField()

    def validate(self, attrs):
        if not verify_code_service.check_verify_code(attrs['mobile'], attrs['verify_code']):
            raise ValidationError({"message": "????????????????????????"})

        if not models.User.objects.filter(mobile=attrs['mobile']).exists():
            raise ValidationError({"message": "????????????????????????"})
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(validators=[validate_password])
    new_password = serializers.CharField(validators=[validate_password])

    def validate(self, attrs):
        if not authenticate(username=self.context['user'].mobile, password=attrs['old_password']):
            raise ValidationError({"message": "??????????????????"})
        return attrs


class BaseCourseOrderSerializer(serializers.ModelSerializer):
    club_id = serializers.IntegerField(source='club.id', read_only=True)
    club_name = serializers.CharField(source='club.name', read_only=True)
    club_address = serializers.CharField(source='club.address', read_only=True)
    club_longitude = serializers.CharField(source='club.longitude', read_only=True)
    club_latitude = serializers.CharField(source='club.latitude', read_only=True)

    class Meta:
        model = models.CourseOrder
        fields = '__all__'


class BoxerCourseOrderSerializer(BaseCourseOrderSerializer):
    user_id = serializers.IntegerField(source='user.pk', read_only=True)
    user_nickname = serializers.CharField(source='user.user_profile.nick_name', read_only=True)
    user_gender = serializers.BooleanField(source='user.user_profile.gender', read_only=True)
    user_avatar = serializers.SerializerMethodField()
    user_type = serializers.CharField(source="user.get_user_type_display", read_only=True)
    identity = serializers.CharField(source='user.identity', read_only=True)
    comment_score = serializers.SerializerMethodField()
    comment_time = serializers.SerializerMethodField()
    comment_content = serializers.SerializerMethodField()
    comment_images = serializers.SerializerMethodField()

    def get_user_avatar(self, instance):
        return instance.user.user_profile.avatar and get_cdn_url(instance.user.user_profile.avatar)

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


class UserCourseOrderSerializer(BaseCourseOrderSerializer):
    boxer_id = serializers.IntegerField(source='boxer.pk', read_only=True)
    boxer_name = serializers.CharField(source='boxer.real_name', read_only=True)
    boxer_gender = serializers.BooleanField(source='boxer.user.user_profile.gender', read_only=True)
    boxer_user_type = serializers.CharField(source="boxer.user.get_user_type_display", read_only=True)
    boxer_avatar = serializers.SerializerMethodField()

    def get_boxer_avatar(self, instance):
        return instance.boxer.user.user_profile.avatar and get_cdn_url(instance.boxer.user.user_profile.avatar)


class BoxerInfoReadOnlySerializer(serializers.ModelSerializer):
    honor_certificate_images = serializers.ListField(child=serializers.CharField())
    allowed_course = serializers.ListField(child=serializers.CharField())
    identity_number = serializers.SerializerMethodField()

    def get_identity_number(self, instance):
        if instance.user == self.context['request'].user:
            return instance.identity_number
        return ""

    class Meta:
        model = models.BoxerIdentification
        exclude = ["created_time", "updated_time", "user"]


class UserProfileSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField()
    boxer_info = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    height = serializers.IntegerField(max_value=999)
    weight = serializers.IntegerField(max_value=999)
    nick_name = serializers.CharField(max_length=10, required=False)
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    money_balance = serializers.SerializerMethodField()
    user_id = serializers.CharField(source="user.id", read_only=True)
    boxer_status = serializers.CharField(source='user.boxer_identification.authentication_state', read_only=True)
    identity = serializers.CharField(source="user.identity", read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    title = serializers.CharField(source="user.title", read_only=True)
    user_type = serializers.CharField(source="user.get_user_type_display", read_only=True)
    has_hotvideo = serializers.BooleanField(source="user.hot_videos.count", read_only=True)
    has_record = serializers.SerializerMethodField()  # ??????????????????
    has_album = serializers.SerializerMethodField()
    is_following_each_other = serializers.SerializerMethodField()  # ??????????????????

    def to_representation(self, instance):
        data = super(UserProfileSerializer, self).to_representation(instance)
        data['nick_name'] = instance.nick_name or DEFAULT_NICKNAME_FORMAT.format(instance.user.id)
        data['avatar'] = get_cdn_url(instance.avatar) if instance.avatar else DEFAULT_AVATAR
        return data

    def get_is_following(self, instance):
        return bool(is_following(self.context['request'].user.id, instance.user.id))

    def get_money_balance(self, instance):
        return instance.user.money_balance

    def get_followers_count(self, instance):
        return follower_count(instance.user.id)

    def get_following_count(self, instance):
        return following_count(instance.user.id)

    def get_mobile(self, instance):
        return instance.user.mobile

    def get_boxer_info(self, instance):
        boxer = models.BoxerIdentification.objects.filter(user=instance.user).first()
        return BoxerInfoReadOnlySerializer(boxer, context=self.context).data

    def get_has_album(self, instance):
        return instance.user.albums.filter(is_show=True).exists()

    def get_has_record(self, instance):
        players = Player.objects.filter(user=instance.user)
        if not players.exists():
            return False
        return Match.objects.filter(Q(red_player=players.first()) | Q(blue_player=players.first()),
                                    schedule__status=SCHEDULE_STATUS_PUBLISHED).exists()

    def get_is_following_each_other(self, instance):
        current_user_id = self.context['request'].user.id
        current_user = User.objects.filter(id=current_user_id)
        if not current_user.exists():  # ???????????????
            return False
        return all([is_following(current_user_id, instance.user_id), is_following(instance.user_id, current_user_id)])

    def validate(self, attrs):
        if attrs.get("nick_name"):
            nick_name_index_letter = hans_to_initial(attrs['nick_name'])
            if not re.match(r"[a-zA-Z]", nick_name_index_letter):
                nick_name_index_letter = "#"
            attrs['nick_name_index_letter'] = nick_name_index_letter
        return attrs

    class Meta:
        model = models.UserProfile
        exclude = ["created_time", "id", "updated_time", "user"]
        read_only_fields = ["alipay_account", "nick_name", "boxer_info", "mobile"]


class ChangeMobileSerializer(serializers.Serializer):
    mobile = serializers.CharField(validators=[validate_mobile])
    verify_code = serializers.CharField()

    def validate(self, attrs):
        if attrs['mobile'] == self.context['request'].user.mobile:
            raise ValidationError({"message": "?????????????????????????????????"})
        if models.User.objects.filter(mobile=attrs['mobile']).exists():
            raise ValidationError({"message": "???????????????????????????????????????????????????"})
        if not verify_code_service.check_verify_code(attrs['mobile'], attrs['verify_code']):
            raise ValidationError({"message": "????????????????????????"})
        return attrs


class NewsSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField()
    content = serializers.SerializerMethodField()
    read_count = serializers.SerializerMethodField()
    pub_time = serializers.DateTimeField(source='updated_time', read_only=True)
    picture = serializers.SerializerMethodField()

    def get_content(self, obj):
        if self.context['request'].query_params.get('in_app') == '1':
            return obj.app_content
        return obj.share_content or obj.app_content

    def get_read_count(self, obj):
        return obj.initial_views_count + obj.views_count

    def get_picture(self, obj):
        return obj.picture and get_cdn_url(obj.picture)

    class Meta:
        model = models.GameNews
        fields = ('id', 'title', 'sub_title', 'content', 'comment_count', 'read_count', 'picture',
                  'stay_top', 'pub_time')


class BlockedUserSerializer(serializers.BaseSerializer):
    def to_representation(self, user):
        representation_dict = {"id": user.id, "user_type": user.get_user_type_display()}
        if hasattr(user, "user_profile"):
            avatar = get_cdn_url(user.user_profile.avatar) if user.user_profile.avatar else None
            representation_dict.update(nick_name=user.user_profile.nick_name, avatar=avatar)
        return representation_dict


class CourseAllowNullDataSerializer(serializers.ModelSerializer):
    club_name = serializers.CharField(source='club.name', read_only=True)
    club_address = serializers.CharField(source='club.address', read_only=True)
    club_longitude = serializers.CharField(source='club.longitude', read_only=True)
    club_latitude = serializers.CharField(source='club.latitude', read_only=True)
    order_count = serializers.IntegerField(read_only=True)
    score = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Course
        fields = '__all__'
        read_only_fields = ('boxer', 'course_name')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        exclude = ('created_time', 'updated_time', 'operator')


class CourseFullDataSerializer(CourseAllowNullDataSerializer):
    price = serializers.IntegerField()
    duration = serializers.IntegerField()
    validity = serializers.DateField()
    is_open = serializers.BooleanField()

    def validate(self, attrs):
        if not attrs['club']:
            raise serializers.ValidationError('???????????????')
        if attrs.get('validity') < datetime.date(datetime.today()):
            raise serializers.ValidationError('??????????????????????????????????????????')
        return attrs


class CourseOrderCommentSerializer(serializers.ModelSerializer):
    user = DiscoverUserField(read_only=True)
    images = serializers.ListField(child=serializers.CharField(), required=False)
    course_name = serializers.CharField(source='order.course_name', read_only=True)

    def validate(self, attrs):
        if attrs['order'].status != constants.COURSE_PAYMENT_STATUS_WAIT_COMMENT:
            raise ValidationError('?????????????????????????????????????????????')
        return attrs

    class Meta:
        model = models.OrderComment
        fields = '__all__'


class MoneyChangeLogReadOnlySerializer(serializers.ModelSerializer):
    change_type = serializers.CharField(source='get_change_type_display')
    created_time = serializers.DateTimeField()
    change_amount = serializers.SerializerMethodField()

    def get_change_amount(self, instance):
        change_amount = instance.change_amount
        # ????????????????????????????????????
        return f"+{change_amount/100:.2f}" if change_amount > 0 else f"{change_amount/100:.2f}"

    class Meta:
        model = models.MoneyChangeLog
        fields = ['change_amount', "change_type", "created_time"]


class RechargeSerializer(serializers.Serializer):
    amount = serializers.IntegerField()


class WithdrawSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display", read_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.user_profile.alipay_account:
            raise ValidationError("??????????????????????????????????????????????????????????????????")
        if attrs['amount'] < WITHDRAW_MIN_CONFINE:
            raise ValidationError(f"????????????????????????{WITHDRAW_MIN_CONFINE/100}???!")
        if attrs['amount'] > user.money_balance:
            raise ValidationError("????????????????????????????????????!")
        attrs['user'] = user
        attrs['withdraw_account'] = user.user_profile.alipay_account
        attrs['order_number'] = datetime.now().strftime(
            f"%Y%m%d{str(redis_client.incr(redis_const.WITHDRAW_ORDER_NUMBER_INCR)).zfill(5)}")
        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        change_money(instance.user, -instance.amount, MONEY_CHANGE_TYPE_REDUCE_WITHDRAW,
                     remarks=f"{instance.order_number}")
        return instance

    class Meta:
        model = models.WithdrawLog
        fields = ['amount', "order_number", "created_time", "status"]
        read_only_fields = ["order_number", "created_time"]


class OrderCommentSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.CharField())
    user = DiscoverUserField(read_only=True)
    course_name = serializers.CharField(source='order.course_name', read_only=True)

    class Meta:
        model = models.OrderComment
        exclude = ('is_deleted',)


class BoxingClubSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.CharField(), read_only=True)
    longitude = serializers.FloatField(read_only=True)
    latitude = serializers.FloatField(read_only=True)

    class Meta:
        model = BoxingClub
        fields = '__all__'


class RechargeLogReadOnlySerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")

    class Meta:
        model = models.PayOrder
        fields = ["out_trade_no", "amount", "id", "order_time", "status"]


class SocialLoginSerializer(serializers.Serializer):
    wechat_openid = serializers.CharField(required=False)
    weibo_openid = serializers.CharField(required=False)

    def validate(self, attrs):
        wechat_openid = attrs.get("wechat_openid")
        weibo_openid = attrs.get("weibo_openid")
        if not wechat_openid and not weibo_openid:
            raise ValidationError("wechat_openid???weibo_openid??????????????????????????????")
        if wechat_openid and weibo_openid:
            raise ValidationError("wechat_openid???weibo_openid??????????????????")
        return attrs


class ContactSerializer(serializers.ModelSerializer):
    nick_name = serializers.CharField(source="user_profile.nick_name")
    index_letter = serializers.CharField(source="user_profile.nick_name_index_letter")
    avatar = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()

    def get_avatar(self, user):
        return user.user_profile.avatar and get_cdn_url(user.user_profile.avatar)

    def get_user_type(self, user):
        return user.get_user_type_display()

    class Meta:
        model = models.User
        fields = ['id', "nick_name", "avatar", "index_letter", "user_type"]


class ShutUpWriteOnlySerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())


class AlbumSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField(source="pictures.count")
    pictures = serializers.SerializerMethodField()

    def get_pictures(self, instance):
        return [{'id': item.id, 'picture': item.picture} for item in instance.pictures.all()[:9]]  # APP???????????????????????????9?????????

    class Meta:
        model = models.Album
        fields = ['id', 'name', 'total', 'pictures']


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    images = serializers.ListField(child=serializers.CharField(max_length=200), max_length=9, required=False)

    class Meta:
        model = models.Feedback
        fields = "__all__"
