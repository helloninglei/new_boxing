# -*- coding: utf-8 -*-

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

mobile_regex = re.compile(r'^1\d{10}$')
identity_number_regex = re.compile(r'^\d{17}[xX0-9]$')
real_name_regex = re.compile(r'^[\u4e00-\u9fa5]{1,6}$')
nation_regex = re.compile(r'^[\u4e00-\u9fa5]{1,5}$')
profession_regex = re.compile(r'^[\u4e00-\u9fa5]{1,10}$')


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
    mobile_or_email_regex = re.compile(r"^1\d{10}$|^[\w.-]+@[\da-zA-Z]+(.[\w-]+)+$")
    if not mobile_or_email_regex.match(value):
        raise ValidationError(_('%(value)s 不是有效邮箱或手机号。'), params={"value": value})


def validate_real_name(value):
    if not real_name_regex.match(value):
        raise ValidationError("真实姓名为不超过6个的汉字")


def validate_nation(value):
    if not nation_regex.match(value):
        raise ValidationError("名族为不超过5个的汉字")


def validate_profession(value):
    if not profession_regex.match(value):
        raise ValidationError("职业为不超过10个的汉字")
