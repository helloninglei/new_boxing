# -*- coding: utf-8 -*-

from rest_framework import serializers
from biz import models
from django.forms.models import model_to_dict


class MessageUserField(serializers.RelatedField):
    def to_representation(self, user):
        return model_to_dict(user.user_profile, fields=('nick_name', 'avatar'))


class MessageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.URLField())
    user = MessageUserField(read_only=True)

    class Meta:
        model = models.Message
        fields = ['id', 'content', 'images', 'video', 'created_time', 'user']
        extra_kwargs = {'images': {'required': False}, 'video': {'required': False}}
