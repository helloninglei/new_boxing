# -*- coding: utf-8 -*-
from rest_framework import permissions


class OnlyOwnerCanDeletePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method != 'DELETE':
            return True
        else:
            if request.user == obj.user:
                return True
            return False


