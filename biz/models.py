# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from biz import constants


class User(AbstractUser):
    first_name = None
    last_name = None
    name = models.CharField(max_length=30, blank=True, null=True)
    weibo_openid = models.CharField(null=True, blank=True, unique=True, max_length=128)
    wechat_openid = models.CharField(null=True, blank=True, unique=True, max_length=128)
    boxing_beans_balance = models.IntegerField(default=0)
    wallet_balance = models.IntegerField(default=0)  # unit, 分

    class Meta(AbstractUser.Meta):
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditBaseModel(BaseModel):
    auditor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+', db_index=False)
    audit_time = models.DateTimeField()

    class Meta:
        abstract = True


class TradeBaseModel(models.Model):
    trade_amount = models.IntegerField()  # unit, 分
    order_id = models.CharField(max_length=128)
    trade_device = models.CharField(choices=constants.DEVICE_CHOICES, max_length=10)
    trade_channel = models.CharField(choices=constants.TRADE_CHANNEL_CHOICES, max_length=10)
    payable_account = models.CharField(max_length=50)
    receivable_account = models.CharField(max_length=50)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    nick_name = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    nation = models.CharField(max_length=30)
    birthday = models.DateTimeField()
    weight = models.CharField(max_length=10)
    stature = models.CharField(max_length=10)
    profession = models.CharField(max_length=20)
    head_portrait = models.URLField()
    gender = models.BooleanField(default=True)  # True-男，False-女
    live_address = models.CharField(max_length=254, null=True, blank=True)
    signature = models.CharField(max_length=30)  # 个性签名
    alipay_account = models.CharField(max_length=30)

    class Meta:
        db_table = 'user_profile'


class UserRelation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    passive_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    is_friend = models.BooleanField(default=False)
    is_black = models.BooleanField(default=False)
    is_follower = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_relation'


class BoxerProfile(AuditBaseModel):
    """拳手认证信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='boxer_profile')
    identity_number = models.CharField(max_length=18)
    mobile = models.CharField(max_length=11)
    is_professional_boxer = models.BooleanField(default=False)  # True, 职业 | False，非职业

    club = models.CharField(max_length=128)
    introduction = models.TextField()

    class Meta:
        db_table = 'boxer_profile'


class BoxerProfileAdditional(BaseModel):
    boxer_profile = models.ForeignKey(BoxerProfile, on_delete=models.CASCADE, related_name='boxer_profile_additional')
    data_url = models.URLField()
    data_type = models.CharField(choices=constants.MEDIA_TYPE_CHOICES, max_length=30)

    class Meta:
        db_table = 'boxer_profile_additional'


class UserBalanceBill(AuditBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_balance_bill')
    balance_type = models.CharField(choices=constants.BALANCE_TYPE_CHOICES, max_length=10)
    balance_bill_type = models.CharField(max_length=10, choices=constants.BALANCE_BILL_TYPE)
    amount = models.IntegerField()  # unit, 分 | + 收入  | - 支出
    remark = models.CharField(null=True, blank=True, max_length=30)

    class Meta:
        db_table = 'user_balance_bill'


class UserPaymentBill(TradeBaseModel, BaseModel):
    """用户支付流水"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payment_bills')
    status = models.CharField(choices=constants.TRADE_STATUS_CHOICES, max_length=10)
    remark = models.CharField(max_length=50, null=True, blank=True)
    bill_type = models.CharField(max_length=20, choices=constants.BILL_TYPE_CHOICES)

    class Meta:
        db_table = 'user_payment_bill'


class UserWithDrawApplication(TradeBaseModel, AuditBaseModel):
    """用户提现申请"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_with_draw_applications')
    status = models.CharField(max_length=50, choices=constants.DRAW_WITH_CHOICES)

    class Meta:
        db_table = 'user_with_draw_application'
