# -*- coding: utf-8 -*-
from rest_framework import permissions


class OnlyOwnerCanDeletePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method != 'DELETE':
            return True
        else:
            return request.user == obj.user
