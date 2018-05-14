from rest_framework.exceptions import ValidationError


class NotStaffUserError(ValidationError):
    pass
