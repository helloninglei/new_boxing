# -*- coding: utf-8 -*-

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_mobile(value):
    mobile_regex = re.compile(r'^1[3-9]\d{9}$')
    if not mobile_regex.match(value):
        raise ValidationError(
            _('%(value)s is not an mobile'), params={'value': value},
        )


def get_one_to_one_model_field(instance, related_name, field=None):
    if field:
        return getattr(getattr(instance, related_name), field) if hasattr(instance, related_name) else None
    return lambda attr: getattr(getattr(instance, related_name), attr) if hasattr(instance, related_name) else None
