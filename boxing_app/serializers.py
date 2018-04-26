# -*- coding: utf-8 -*-
from rest_framework import serializers

from biz.models import BoxerIdentification, BoxerMediaAdditional, User


class BoxerMediaAdditionalSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoxerMediaAdditional
        fields = ['media_url', 'media_type']


class BoxerIdentificationSerializer(serializers.ModelSerializer):
    boxer_identification_additional = BoxerMediaAdditionalSerializer(many=True)
    height = serializers.IntegerField(max_value=250, min_value=100)
    weight = serializers.IntegerField(max_value=999)

    def create(self, validated_data):
        user = self.context['request'].user
        identification_addition_data = validated_data.pop('boxer_identification_additional')
        print identification_addition_data
        boxer_identification = BoxerIdentification.objects.create(user=user,**validated_data)
        for additiona_data in identification_addition_data:
            BoxerMediaAdditional.objects.create(boxer_identification=boxer_identification, **additiona_data)
        return boxer_identification

    class Meta:
        model = BoxerIdentification
        fields = ['real_name', 'height', 'weight', 'birthday', 'identity_number', 'mobile', 'is_professional_boxer',
                  'club', 'introduction', 'experience', 'boxer_identification_additional']