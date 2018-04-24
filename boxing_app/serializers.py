# -*- coding: utf-8 -*-

from rest_framework import serializers
from biz import models


class MessageSerializer(serializers.ModelSerializer):
    images = serializers.ListField()
    class Meta:
        model = models.Message
        fields = ['id', 'content', 'images', 'video', 'created_time', 'user']
