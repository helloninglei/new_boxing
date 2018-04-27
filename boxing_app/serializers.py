# -*- coding: utf-8 -*-

from rest_framework import serializers
from biz import models
from django.forms.models import model_to_dict


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

    class Meta:
        model = models.Message
        fields = ['id', 'content', 'images', 'video', 'created_time', 'user']

class BaseCommentSerializer(serializers.ModelSerializer):
    user = DiscoverUserField(read_only=True)
    to_user = DiscoverUserField(read_only=True)

    class Meta:
        model = models.Comment
        fields = ['id', 'content', 'user', 'to_user']


class CommentSerializer(serializers.ModelSerializer):
    user = DiscoverUserField(read_only=True)
    replies = serializers.SerializerMethodField()

    def get_replies(self, obj):
        count = obj.reply_list().count()
        latest_two = obj.reply_list()[:2]
        return {
            'count': count,
            'results': BaseCommentSerializer(latest_two, many=True).data
        }

    class Meta:
        model = models.Comment
        fields = ['id', 'content', 'user', 'replies']


class ReplySerializer(CommentSerializer):
    def get_replies(self, obj):
        count = obj.reply_list().count()
        latest = obj.reply_list()
        return {
            'count': count,
            'results': BaseCommentSerializer(latest,  many=True).data
        }