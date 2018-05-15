# -*- coding: utf-8 -*-

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

mobile_regex = re.compile(r'^1\d{10}$')
identity_number_regex = re.compile(r'^\d{17}[xX0-9]$')


def validate_mobile(value):
    if not mobile_regex.match(value):
        raise ValidationError(
            _('%(value)s 不是有效手机号。'), params={'value': value},
        )


def validate_identity_number(value):
    if identity_number_regex.match(value) is None:
        raise ValidationError("身份证号码格式错误！")


def validate_password(value):
    password_regex = re.compile(r"^[\da-zA-Z]{6,16}$")
    if not password_regex.match(value):
        raise ValidationError("密码为6-16位数字字母组合！")


def validate_mobile_or_email(value):
    email_regex = re.compile(r"^1\d{10}|[\w.-]+@[\da-zA-Z]+(.[\w-]+)+$")
    if not email_regex.match(value):
        raise ValidationError(_('%(value)s 不是有效邮箱或手机号。'), params={"value": value})
