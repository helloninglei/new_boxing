# -*- coding: utf-8 -*-
from rest_framework import permissions

from biz import models, constants


class OnlyOwnerCanDeletePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method != 'DELETE':
            return True
        return request.user == obj.user


class OnlyBoxerSelfCanConfirmOrderPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.course.boxer.user == request.user:
            return True


class IsBoxerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return models.BoxerIdentification.objects.filter(user=request.user,
                                                         authentication_state=constants.BOXER_AUTHENTICATION_STATE_APPROVED).exists()
