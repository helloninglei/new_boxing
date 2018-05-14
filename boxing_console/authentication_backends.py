from django.contrib.auth.backends import ModelBackend
from biz.validation_errors import NotStaffUserError


class StaffUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        if user and not user.is_staff:
            raise NotStaffUserError({"message": "该账号无登录权限!"})
        return user
