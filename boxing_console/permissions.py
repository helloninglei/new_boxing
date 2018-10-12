from rest_framework import permissions
from biz.constants import VERSION_MANAGER_GROUP


class IsSuperAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class VersionReleasePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.id in VERSION_MANAGER_GROUP
