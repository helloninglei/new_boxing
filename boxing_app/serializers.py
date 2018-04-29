# -*- coding: utf-8 -*-

from rest_framework import serializers
from biz import models
from biz.constants import DISCOVER_MESSAGE_REPORT_OTHER_REASON
from django.forms.models import model_to_dict
from rest_framework.exceptions import ValidationError


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


class LikeSerializer(serializers.ModelSerializer):
    user = DiscoverUserField(read_only=True)

    class Meta:
        model = models.Like
        fields = ['user', 'created_time']


class ReportSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['reason'] == DISCOVER_MESSAGE_REPORT_OTHER_REASON and not data['remark']:
            raise ValidationError({'remark': ['remark is required']})
        return data

    class Meta:
        model = models.Report
        fields = ['reason', 'remark']
