# -*- coding: utf-8 -*-

from rest_framework import serializers
from biz import models


class MessageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.URLField())

    class Meta:
        model = models.Message
        fields = ['id', 'content', 'images', 'video', 'created_time', 'user']
        read_only_fields = ['user']
        extra_kwargs = {'images': {'required': False}, 'video': {'required': False}}

