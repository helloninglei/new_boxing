from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.serializers import AuthTokenSerializer
from biz import models
from biz.validator import validate_mobile
from biz.services.captcha_service import check_captcha
from biz import redis_client, redis_const
from biz.validation_errors import NotStaffUserError


class AuthTokenLoginSerializer(AuthTokenSerializer):
    username = serializers.CharField(label=_("Username"), validators=[validate_mobile])
    captcha = serializers.JSONField(required=False if settings.PROJECT_PROPERTY == settings.PROJECT_API else True)

    def validate(self, attrs):
        if "captcha" in attrs:
            captcha = attrs['captcha']
            if not check_captcha(captcha.get('captcha_code'), captcha.get("captcha_hash")):
                raise ValidationError({"message": "图形验证码错误！"})
        else:
            if redis_client.redis_client.exists(redis_const.HAS_LOGINED.format(mobile=attrs['username'])) \
                    or settings.PROJECT_PROPERTY == settings.PROJECT_CONSOLE:
                raise ValidationError({"message": "需要图形验证码!"})

        if not models.User.objects.filter(mobile=attrs['username']).exists():
            raise ValidationError({"message": "手机号未注册！"})
        redis_client.redis_client.setex(
            redis_const.HAS_LOGINED.format(mobile=attrs['username']), redis_const.LOGIN_INTERVAL, "1")
        try:
            attrs = super().validate(attrs)
        except NotStaffUserError as e:
            raise e
        except serializers.ValidationError:
            raise ValidationError({"message": "用户名或密码错误!"})
        return attrs
