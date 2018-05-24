# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.forms.models import model_to_dict
from rest_framework.exceptions import ValidationError
from rest_framework.compat import authenticate
from biz.constants import BOXER_AUTHENTICATION_STATE_WAITING
from biz.models import PayOrder, BoxingClub, OrderComment, Course
from biz.constants import PAYMENT_TYPE
from biz.constants import REPORT_OTHER_REASON
from biz.constants import MESSAGE_TYPE_ONLY_TEXT, MESSAGE_TYPE_HAS_IMAGE, MESSAGE_TYPE_HAS_VIDEO
from biz.redis_client import is_following
from biz import models, constants
from biz.services.pay_service import PayService
from biz.validator import validate_mobile, validate_password, validate_mobile_or_email
from biz.services.captcha_service import check_captcha
from biz import redis_client, redis_const
from biz.redis_const import SEND_VERIFY_CODE
from boxing_app.services import verify_code_service
from biz.utils import get_client_ip, get_device_platform


class BoxerIdentificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    honor_certificate_images = serializers.ListField(child=serializers.CharField(), required=False)
    competition_video = serializers.CharField(required=False)
    height = serializers.IntegerField(max_value=250, min_value=100)
    weight = serializers.IntegerField(max_value=999)

    def update(self, instance, validated_data):
        validated_data['authentication_state'] = BOXER_AUTHENTICATION_STATE_WAITING
        return super().update(instance, validated_data)

    class Meta:
        model = models.BoxerIdentification
        fields = '__all__'
        read_only_fields = ('authentication_state', 'is_locked')


class DiscoverUserField(serializers.RelatedField):
    def to_representation(self, user):
        result = {
            'id': user.id,
            'identity': user.identity,
            'is_following': bool(is_following(self.context['request'].user.id, user.id)),
            'nick_name': None,
            'avatar': None,
        }

        if hasattr(user, 'user_profile'):
            profile = model_to_dict(user.user_profile, fields=('nick_name', 'avatar'))
            result.update(profile)
        return result


class MessageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.CharField(max_length=200), required=False)
    video = serializers.CharField(max_length=200, required=False)
    user = DiscoverUserField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    is_like = serializers.BooleanField(read_only=True)
    msg_type = serializers.SerializerMethodField()

    def get_msg_type(self, obj):
        if obj.video:
            return MESSAGE_TYPE_HAS_VIDEO
        if obj.images:
            return MESSAGE_TYPE_HAS_IMAGE
        return MESSAGE_TYPE_ONLY_TEXT

    def validate(self, data):
        if data.get('video') and data.get('images'):
            raise ValidationError({'video': ['视频和图片不可同时上传']})
        return data

    class Meta:
        model = models.Message
        fields = ['id', 'content', 'images', 'video', 'msg_type', 'created_time', 'user', 'like_count', 'comment_count',
                  'is_like']


class BasicReplySerializer(serializers.ModelSerializer):
    user = DiscoverUserField(read_only=True)
    to_user = DiscoverUserField(read_only=True)

    class Meta:
        model = models.Comment
        fields = ['id', 'content', 'user', 'to_user']


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
        fields = ['id', 'content', 'user', 'replies']


class LikeSerializer(serializers.ModelSerializer):
    user = DiscoverUserField(read_only=True)

    class Meta:
        model = models.Like
        fields = ['user', 'created_time']


class ReportSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['reason'] == REPORT_OTHER_REASON and not data.get('remark'):
            raise ValidationError({'remark': ['举报理由是必填项']})
        return data

    class Meta:
        model = models.Report
        fields = ['id', 'object_id', 'reason', 'remark']


class FollowUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    avatar = serializers.SerializerMethodField()
    nick_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    def _get_profile(self, user):
        if hasattr(user, 'user_profile'):
            return user.user_profile
        return {}

    def get_avatar(self, user):
        return self._get_profile(user).get('avatar')

    def get_nick_name(self, user):
        return self._get_profile(user).get('nick_name')

    def get_address(self, user):
        return self._get_profile(user).get('address')

    def get_bio(self, user):
        return self._get_profile(user).get('bio')

    def get_is_following(self, user):
        current_user_id = self.context['current_user_id']
        return bool(is_following(current_user_id, user.id))

    class Meta:
        fields = ['id', 'avatar', 'nick_name', 'address', 'bio', 'is_follow']
        read_only_fields = '__all__'


class SendVerifyCodeSerializer(serializers.Serializer):
    mobile = serializers.CharField(validators=[validate_mobile])
    captcha = serializers.JSONField(required=False)

    def validate(self, attrs):
        if "captcha" in attrs:
            captcha = attrs['captcha']
            if not check_captcha(captcha.get("captcha_code"), captcha.get("captcha_hash")):
                raise ValidationError({"message": "图形验证码错误！"})
        else:
            if redis_client.redis_client.exists(SEND_VERIFY_CODE.format(mobile=attrs['mobile'])):
                raise ValidationError({"message": "需要图形验证码！"})
        return attrs


class RegisterSerializer(serializers.Serializer):
    mobile = serializers.CharField(validators=[validate_mobile])
    password = serializers.CharField(validators=[validate_password])
    verify_code = serializers.CharField()

    def validate(self, attrs):
        if models.User.objects.filter(mobile=attrs['mobile']).exists():
            raise ValidationError({"message": "手机号已存在！"})
        if not verify_code_service.check_verify_code(mobile=attrs['mobile'], verify_code=attrs['verify_code']):
            raise ValidationError({"message": "短信验证码错误！"})
        return attrs


class RegisterWithInfoSerializer(serializers.Serializer):
    avatar = serializers.CharField()
    gender = serializers.BooleanField()
    nick_name = serializers.CharField()
    mobile = serializers.CharField(validators=[validate_mobile])

    def validate(self, attrs):
        if not redis_client.redis_client.exists(redis_const.REGISTER_INFO.format(mobile=attrs['mobile'])):
            raise ValidationError({"message": "手机号未注册！无法提交个人资料！"})
        return attrs


class HotVideoSerializer(serializers.ModelSerializer):
    is_paid = serializers.BooleanField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        if obj.is_paid:
            return obj.url

    class Meta:
        model = models.HotVideo
        fields = ('id', 'name', 'description', 'is_paid', 'comment_count', 'url', 'try_url', 'price', 'created_time')


class LoginIsNeedCaptchaSerializer(serializers.Serializer):
    mobile = serializers.CharField(validators=[validate_mobile])


class PaySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    device = serializers.SerializerMethodField()
    ip = serializers.SerializerMethodField()
    payment_type = serializers.ChoiceField(choices=PAYMENT_TYPE)
    content_object = serializers.SerializerMethodField()

    def get_content_object(self, obj):
        object_type = self.context['object_type'].title().replace('_', '')
        return getattr(models, object_type).objects.get(pk=obj['id'])

    def get_ip(self, obj):
        return get_client_ip(self.context['request'])

    def get_device(self, obj):
        return get_device_platform(self.context['request'])


class BindAlipayAccountSerializer(serializers.Serializer):
    verify_code = serializers.CharField()
    alipay_account = serializers.CharField(validators=[validate_mobile_or_email])

    def validate(self, attrs):
        if not verify_code_service.check_verify_code(self.context['user'].mobile, attrs['verify_code']):
            raise ValidationError({"message": "短信验证码错误！"})
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(validators=[validate_password])
    mobile = serializers.CharField(validators=[validate_mobile])
    verify_code = serializers.CharField()

    def validate(self, attrs):
        if not verify_code_service.check_verify_code(attrs['mobile'], attrs['verify_code']):
            raise ValidationError({"message": "短信验证码错误！"})

        if not models.User.objects.filter(mobile=attrs['mobile']).exists():
            raise ValidationError({"message": "该手机号未注册！"})
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(validators=[validate_password])
    new_password = serializers.CharField(validators=[validate_password])

    def validate(self, attrs):
        if not authenticate(username=self.context['user'].mobile, password=attrs['old_password']):
            raise ValidationError({"message": "原密码错误！"})
        return attrs


class BaseCourseOrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    content_type = serializers.CharField(read_only=True)
    object_id = serializers.IntegerField(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    out_trade_no = serializers.IntegerField(read_only=True)
    device = serializers.IntegerField(read_only=True)
    course_name = serializers.CharField(source='content_object.course_name', read_only=True)
    course_duration = serializers.IntegerField(source='content_object.duration', read_only=True)
    course_validity = serializers.DateField(source='content_object.validity', read_only=True)
    course_price = serializers.IntegerField(source='content_object.price', read_only=True)
    club_name = serializers.CharField(source='content_object.club.name', read_only=True)
    club_address = serializers.CharField(source='content_object.club.address', read_only=True)
    club_longitude = serializers.CharField(source='content_object.club.longitude', read_only=True)
    club_latitude = serializers.CharField(source='content_object.club.latitude', read_only=True)

    def validate(self, attrs):
        if not Course.objects.filter(id=attrs['course_id']).exists():
            raise ValidationError('课程不存在')
        attrs['object_id'] = attrs['course_id']
        attrs.pop('course_id')
        attrs['content_type'] = ContentType.objects.get(app_label="biz", model="course")
        attrs['user'] = self.context['request'].user
        attrs['out_trade_no'] = PayService.generate_out_trade_no()
        attrs['device'] = get_device_platform(self.context['request'])
        return attrs

    class Meta:
        model = PayOrder
        fields = '__all__'


class BoxerCourseOrderSerializer(BaseCourseOrderSerializer):
    user_id = serializers.IntegerField(source='user.pk', read_only=True)
    user_nickname = serializers.CharField(source='user.user_profile.nick_name', read_only=True)
    user_gender = serializers.BooleanField(source='user.user_profile.gender', read_only=True)
    user_avatar = serializers.CharField(source='user.user_profile.avatar', read_only=True)
    comment_score = serializers.SerializerMethodField()
    comment_time = serializers.SerializerMethodField()
    comment_content = serializers.SerializerMethodField()
    comment_images = serializers.SerializerMethodField()

    def get_comment_score(self, instance):
        comment = self.get_comment(instance)
        return comment.score if comment else None

    def get_comment_time(self, instance):
        comment = self.get_comment(instance)
        return comment.created_time if comment else None

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
    boxer_id = serializers.IntegerField(source='content_object.boxer.pk', read_only=True)
    boxer_name = serializers.CharField(source='content_object.boxer.real_name', read_only=True)
    boxer_gender = serializers.BooleanField(source='content_object.boxer.user.user_profile.gender', read_only=True)
    boxer_avatar = serializers.CharField(source='content_object.boxer.user.user_profile.avatar',read_only=True)


class BoxerInfoReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BoxerIdentification
        fields = ["birthday", "introduction", "job", "experience", "height", "honor_certificate_images",
                  "is_professional_boxer", "real_name", "weight", "club", "mobile"]


class UserProfileSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField()
    boxer_info = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    height = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=30)
    nation = serializers.CharField(max_length=30)
    profession = serializers.CharField(max_length=20)
    weight = serializers.CharField(max_length=10)
    nick_name = serializers.CharField(max_length=10, required=False)
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    money_balance = serializers.SerializerMethodField()
    boxer_status = serializers.CharField(source='user.boxer_identification.authentication_state', read_only=True)

    def get_money_balance(self, instance):
        return instance.user.money_balance

    def get_followers_count(self, instance):
        return redis_client.follower_count(instance.id)

    def get_following_count(self, instance):
        return redis_client.following_count(instance.id)

    def get_mobile(self, instance):
        return instance.user.mobile

    def get_boxer_info(self, instance):
        return BoxerInfoReadOnlySerializer(models.BoxerIdentification.objects.filter(user=instance.user).first()).data

    class Meta:
        model = models.UserProfile
        exclude = ["created_time", "id", "updated_time", "user"]
        read_only_fields = ["alipay_account", "gender", "nick_name", "boxer_info", "mobile"]


class ChangeMobileSerializer(serializers.Serializer):
    mobile = serializers.CharField(validators=[validate_mobile])
    verify_code = serializers.CharField()

    def validate(self, attrs):
        if attrs['mobile'] == self.context['request'].user.mobile:
            raise ValidationError({"message": "手机号和原手机号相同！"})
        if models.User.objects.filter(mobile=attrs['mobile']).exists():
            raise ValidationError({"message": "手机号已绑定一个账号，不能再绑定！"})
        if not verify_code_service.check_verify_code(attrs['mobile'], attrs['verify_code']):
            raise ValidationError({"message": "短信验证码错误！"})
        return attrs


class NewsSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField()
    content = serializers.SerializerMethodField()
    read_count = serializers.SerializerMethodField()

    def get_content(self, obj):
        if self.context['request'].META.get('source'):
            return obj.app_content
        return obj.share_content or obj.app_content

    def get_read_count(self, obj):
        return obj.initial_views_count + obj.views_count

    class Meta:
        model = models.GameNews
        fields = ('id', 'title', 'sub_title', 'content', 'comment_count', 'created_time', 'read_count', 'picture',
                  'stay_top')


class BlockedUserSerializer(serializers.BaseSerializer):

    def to_representation(self, user):
        representation_dict = {"id": user.id}
        if hasattr(user, "user_profile"):
            representation_dict.update(nick_name=user.user_profile.nick_name, avatar=user.user_profile.avatar)
        return representation_dict


class CourseAllowNullDataSerializer(serializers.ModelSerializer):
    club_name = serializers.CharField(source='club.name', read_only=True)
    club_address = serializers.CharField(source='club.address', read_only=True)
    club_longitude = serializers.CharField(source='club.longitude', read_only=True)
    club_latitude = serializers.CharField(source='club.latitude', read_only=True)

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
            raise serializers.ValidationError('拳馆不存在')
        return attrs


class CourseOrderCommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    images = serializers.ListField(child=serializers.CharField(), required=False)

    def validate(self, attrs):
        if  attrs['order'].status != constants.PAYMENT_STATUS_WAIT_COMMENT:
            raise ValidationError('订单不是未评论状态，不能评论！')
        return attrs

    class Meta:
        model = models.OrderComment
        fields = '__all__'
