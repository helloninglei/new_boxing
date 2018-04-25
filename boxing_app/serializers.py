# -*- coding: utf-8 -*-
from rest_framework import serializers

from biz.models import BoxerIdentification, BoxerMediaAdditional


class BoxerMediaAdditionalSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoxerMediaAdditional
        fields = '__all__'


class BoxerIdentificationSerializer(serializers.ModelSerializer):
    media_addition = BoxerMediaAdditionalSerializer(many=True)
    height = serializers.IntegerField(max_value=250, min_value=100)
    weight = serializers.IntegerField(max_value=999)

    def create(self, validated_data):
        media_addition_data = validated_data.pop('media_additional')
        boxer_identification = BoxerIdentification.objects.create(**validated_data)
        for additional_data in media_addition_data:
            BoxerMediaAdditional.objects.create(boxer_identification=boxer_identification, **additional_data)
        return boxer_identification

    class Meta:
        model = BoxerIdentification
        fields = ['real_name', 'height', 'weight', 'birthday', 'identity_number', 'mobile', 'is_professional_boxer',
                  'club', 'introduction', 'experience', 'media_additional']