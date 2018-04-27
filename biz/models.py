# -*- coding: utf-8 -*-
import json
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from biz import validator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, mobile, password, **extra_fields):
        """
        Creates and saves a User with the given username, and password.
        """
        if not mobile:
            raise ValueError('The given mobile must be set')
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None
    email = None
    username = None
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'mobile'

    objects = UserManager()

    mobile = models.CharField(max_length=11, unique=True, db_index=True, validators=[validator.validate_mobile],
                              error_messages={'unique': u"手机号已存在。"})
    weibo_openid = models.CharField(null=True, blank=True, unique=True, max_length=128)
    wechat_openid = models.CharField(null=True, blank=True, unique=True, max_length=128)

    class Meta(AbstractUser.Meta):
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-id']


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    nick_name = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    nation = models.CharField(max_length=30, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    weight = models.CharField(max_length=10, blank=True, null=True)
    height = models.CharField(max_length=10, blank=True, null=True)
    profession = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.URLField(null=True, blank=True)
    gender = models.BooleanField(default=True)  # True-男，False-女
    address = models.CharField(max_length=254, null=True, blank=True)
    bio = models.CharField(max_length=30, blank=True, null=True)  # 个性签名
    alipay_account = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'user_profile'


class StringListField(models.TextField):
    def get_prep_value(self, value):
        if value:
            return json.dumps(value)

    def from_db_value(self, value, *args):
        if not value:
            return []
        return json.loads(value)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super(SoftDeleteManager, self).get_queryset().filter(is_deleted=False)


# 动态
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='messages')
    content = models.CharField(max_length=140)
    images = StringListField(null=True)
    video = models.URLField(null=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = SoftDeleteManager()

    class Meta:
        db_table = 'discover_message'
        ordering = ('-created_time',)


class Comment(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comments')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='comments', db_index=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = SoftDeleteManager()

    class Meta:
        db_table = 'discover_comment'
        ordering = ('-created_time',)

    def reply_list(self):
        return self.__class__.objects.filter(parent=self)