# -*- coding: utf-8 -*-

from rest_framework import serializers
from biz.models import User
from biz import utils


class UserSerializer(serializers.ModelSerializer):
    nick_name = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H-%M-%S')
    user_basic_info = serializers.SerializerMethodField()

    def get_user_basic_info(self, instance):
        return {field: self._get_user_profile_field(instance, field) for field in ['name', 'nation', 'birthday',
                                                                                   'height', 'weight', 'profession']}

    def get_address(self, instance):
        return self._get_user_profile_field(instance, 'address')

    def get_gender(self, instance):
        return self._get_user_profile_field(instance, 'gender')

    def get_nick_name(self, instance):
        return self._get_user_profile_field(instance, 'nick_name')

    def _get_user_profile_field(self, instance, field=None):
        return utils.get_one_to_one_model_field(instance, 'user_profile', field=field)

    class Meta:
        model = User
        fields = ['id', 'username', 'nick_name', 'mobile', 'gender', 'address', 'coin_balance', 'money_balance',
                  'date_joined', 'user_basic_info']
