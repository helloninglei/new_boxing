# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.forms.models import model_to_dict
from rest_framework.exceptions import ValidationError
from biz.constants import DISCOVER_MESSAGE_REPORT_OTHER_REASON

from biz import models, constants


class BoxerIdentificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    honor_certificate_images = serializers.ListField(child=serializers.URLField(), required=False)
    competition_video = serializers.URLField(required=False)
    height = serializers.IntegerField(max_value=250, min_value=100)
    weight = serializers.IntegerField(max_value=999)

    def update(self, instance, validated_data):
        validated_data['authentication_state'] = constants.BOXER_AUTHENTICATION_STATE_WAITING
        return super().update(instance, validated_data)


    class Meta:
        model = models.BoxerIdentification
        fields = '__all__'
        read_only_fields = ('authentication_state','lock_state')



class DiscoverUserField(serializers.RelatedField):
    def to_representation(self, user):
        result = {'id': user.id}
        if hasattr(user, 'user_profile'):
            profile = model_to_dict(user.user_profile, fields=('nick_name', 'avatar'))
            result.update(profile)
        return result


class MessageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.URLField(), required=False)
    video = serializers.URLField(required=False)
    user = DiscoverUserField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    is_like = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Message
        fields = ['id', 'content', 'images', 'video', 'created_time', 'user', 'like_count', 'comment_count', 'is_like']


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
            'results': BasicReplySerializer(latest,  many=True).data
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
        if data['reason'] == DISCOVER_MESSAGE_REPORT_OTHER_REASON and not data.get('remark'):
            raise ValidationError({'remark': ['举报理由是必填项']})
        return data

    class Meta:
        model = models.Report
        fields = ['object_id', 'reason', 'remark']


class BaseFollowSerializer(serializers.Serializer):
    user_id = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    nick_name = serializers.SerializerMethodField()

    def _get_profile(self, obj):
        user = self._get_user(obj)
        if hasattr(user, 'user_profile'):
            return user.user_profile
        return {}

    def get_user_id(self, obj):
        return self._get_user(obj).id

    def get_avatar(self, obj):
        return self._get_profile(obj).get('avatar')

    def get_nick_name(self, obj):
        return self._get_profile(obj).get('nick_name')

    def get_address(self, obj):
        return self._get_profile(obj).get('address')

    def get_bio(self, obj):
        return self._get_profile(obj).get('bio')

    class Meta:
        model = models.Follow
        fields = ['id', 'user_id', 'avatar', 'nick_name', 'address', 'bio', 'is_follow']
        read_only_fields = '__all__'


# 粉丝列表
class FollowerSerializer(BaseFollowSerializer):

    def _get_user(self, obj):
        return obj.follower


# 关注列表
class FollowedSerializer(BaseFollowSerializer):

    def _get_user(self, obj):
        return obj.user
