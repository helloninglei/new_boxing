# -*- coding: utf-8 -*-
from rest_framework import permissions

from biz import models


class OnlyOwnerCanDeletePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method != 'DELETE':
            return True
        return request.user == obj.user


class IsBoxerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return models.BoxerIdentification.objects.filter(user=request.user).exists()
