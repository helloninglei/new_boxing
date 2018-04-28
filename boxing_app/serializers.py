# -*- coding: utf-8 -*-
from django.db.transaction import atomic
from rest_framework import serializers
from biz import models, constants
from django.forms.models import model_to_dict


from biz.models import BoxerIdentification, BoxerMediaAdditional


class BoxerMediaAdditionalSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoxerMediaAdditional
        fields = ['media_url', 'media_type']


class BoxerIdentificationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    boxer_identification_additional = BoxerMediaAdditionalSerializer(many=True)
    height = serializers.IntegerField(max_value=250, min_value=100)
    weight = serializers.IntegerField(max_value=999)

    @atomic
    def create(self, validated_data):
        identification_addition_data = validated_data.pop('boxer_identification_additional')
        instance = BoxerIdentification.objects.create(**validated_data)
        self.create_addition(instance, identification_addition_data)
        return instance

    @atomic
    def update(self, instance, validated_data):
        instance.real_name = validated_data.get('real_name', instance.real_name)
        instance.height = validated_data.get('height', instance.height)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.identity_number = validated_data.get('identity_number', instance.identity_number)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.is_professional_boxer = validated_data.get('is_professional_boxer', instance.is_professional_boxer)
        instance.club = validated_data.get('club', instance.club)
        instance.job = validated_data.get('job', instance.job)
        instance.introduction = validated_data.get('introduction', instance.introduction)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.authentication_state = constants.BOXER_AUTHENTICATION_STATE_WAITING
        instance.save()

        BoxerMediaAdditional.objects.filter(boxer_identification=instance).delete()
        identification_addition_data = validated_data.get('boxer_identification_additional')
        self.create_addition(instance,identification_addition_data)

        return instance

    def create_addition(self, instance, addition_data_list):
        for additiona_data in addition_data_list:
            BoxerMediaAdditional.objects.create(boxer_identification=instance, **additiona_data)


    class Meta:
        model = BoxerIdentification
        fields = '__all__'
        read_only_fields = ('authentication_state','lock_state')


class MessageUserField(serializers.RelatedField):
    def to_representation(self, user):
        result = {'id': user.id}
        if hasattr(user, 'user_profile'):
            profile = model_to_dict(user.user_profile, fields=('nick_name', 'avatar'))
            result.update(profile)
        return result


class MessageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.URLField(), required=False)
    video = serializers.URLField(required=False)
    user = MessageUserField(read_only=True)

    class Meta:
        model = models.Message
        fields = ['id', 'content', 'images', 'video', 'created_time', 'user']
