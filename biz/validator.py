# -*- coding: utf-8 -*-

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_mobile(value):
    mobile_regex = re.compile(r'^1\d{10}$')
    if not mobile_regex.match(value):
        raise ValidationError(
            _('%(value)s is not an mobile'), params={'value': value},
        )

def validate_identity_number(value):
    identity_number_regex = re.compile(r'^\d{18}$')
    if identity_number_regex.match(value) == None:
        raise ValidationError( "身份证号码格式错误！")
