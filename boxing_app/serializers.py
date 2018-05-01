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
        identification_addition_data =validated_data.pop('boxer_identification_additional')

        [setattr(instance, key, value) for key, value in validated_data.items()]
        instance.approve_state = constants.BOXER_APPROVE_STATE_WAITING

        instance.save()

        BoxerMediaAdditional.objects.filter(boxer_identification=instance).delete()
        self.create_addition(instance,identification_addition_data)

        return instance

    def create_addition(self, instance, addition_data_list):
        boxer_addition_obj_list = [BoxerMediaAdditional(boxer_identification=instance, **additiona_data)
                                   for additiona_data in addition_data_list]
        BoxerMediaAdditional.objects.bulk_create(boxer_addition_obj_list)


    class Meta:
        model = BoxerIdentification
        fields = '__all__'
        read_only_fields = ('approve_state','lock_state')


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
