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
