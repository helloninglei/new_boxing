# -*- coding: utf-8 -*-
from rest_framework import serializers

from biz.models import BoxerIdentification, BoxerMediaAdditional


class BoxerMediaAdditionalSerializer(serializers.ModelSerializer):
    real_name = serializers.CharField(max_length=10)
    height = serializers.IntegerField(max_value=250,min_value=100)
    weight = serializers.IntegerField(max_value=999)

    class Meta:
        model = BoxerMediaAdditional
        fields = ['real_name', 'height', 'weight', 'birthday', 'identity_number', 'mobile', 'is_professional_boxer',
                  'club', 'introduction', 'experience']

class BoxerIdentificationSerializer(serializers.ModelSerializer):
    media_additional = BoxerMediaAdditionalSerializer(many=True, read_only=True)
    class Meta:
        model = BoxerIdentification
        fields = '__all__'