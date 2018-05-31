# -*- coding: utf-8 -*-
from datetime import datetime
from json import loads, dumps
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import ContentType, GenericForeignKey, GenericRelation
from django.core.validators import MinValueValidator

from biz import validator, constants
from biz.constants import USER_IDENTITY_DICT

OFFICIAL_USER_IDS = USER_IDENTITY_DICT.values()
USER_IDENTITY_DICT_REVERSED = {v: k for k, v in USER_IDENTITY_DICT.items()}


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
                              error_messages={'unique': "手机号已存在。"})
    weibo_openid = models.CharField(null=True, blank=True, unique=True, max_length=128)
    wechat_openid = models.CharField(null=True, blank=True, unique=True, max_length=128)
    coin_balance = models.IntegerField(default=0)
    money_balance = models.IntegerField(default=0)  # unit, 分

    @property
    def identity(self):
        if hasattr(self, 'boxer_identification') and self.boxer_identification.authentication_state == \
                constants.BOXER_AUTHENTICATION_STATE_APPROVED:
            return 'boxer'
        user_id = self.id
        if user_id not in OFFICIAL_USER_IDS:
            return 'user'
        return USER_IDENTITY_DICT_REVERSED[user_id]

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


class PropertyChangeLog(BaseModel):
    last_amount = models.IntegerField(default=0)  # 变动前额度, 单位：分
    change_amount = models.IntegerField(default=0)  # 变动额度, 单位：分
    remain_amount = models.IntegerField(default=0)  # 变动后额度, 单位：分
    operator = models.ForeignKey(User, on_delete=models.PROTECT)  # 操作人
    remarks = models.CharField(null=True, max_length=50)  # 备注

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    nick_name = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    nation = models.CharField(max_length=30, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    weight = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    profession = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.CharField(null=True, blank=True, max_length=128)
    gender = models.BooleanField(default=True)  # True-男，False-女
    address = models.CharField(max_length=254, null=True, blank=True)
    bio = models.CharField(max_length=30, blank=True, null=True)  # 个性签名
    alipay_account = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'user_profile'


class CoinChangeLog(PropertyChangeLog):
    user = models.ForeignKey(User, on_delete=models.deletion.PROTECT, related_name='coin_change_log')
    change_type = models.CharField(null=True, max_length=64,
                                   choices=constants.COIN_CHANGE_TYPE_CHOICES)

    class Meta:
        db_table = 'coin_change_log'
        ordering = ['-created_time', '-id']


class MoneyChangeLog(PropertyChangeLog):
    user = models.ForeignKey(User, on_delete=models.deletion.PROTECT, related_name='money_change_log')
    change_type = models.CharField(null=True, max_length=64,
                                   choices=constants.MONEY_CHANGE_TYPE_CHOICES)

    class Meta:
        db_table = 'money_change_log'
        ordering = ['-created_time', '-id']


class StringListField(models.TextField):
    def value_to_string(self, value):
        return self.value_from_object(value)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return loads(value)

    def get_prep_value(self, value):
        if value:
            return dumps(value)

    def from_db_value(self, value, *args):
        if not value:
            return []
        return loads(value)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.save()


# 动态
class Message(SoftDeleteModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='messages')
    content = models.CharField(max_length=140)
    images = StringListField(null=True)
    video = models.CharField(max_length=200, null=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True)
    comments = GenericRelation('Comment')
    reports = GenericRelation('Report')

    class Meta:
        db_table = 'discover_message'
        ordering = ('-created_time',)
        verbose_name = '动态'


# 拳手认证
class BoxerIdentification(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='boxer_identification')
    real_name = models.CharField(max_length=10)
    height = models.IntegerField()  # 单位：cm
    weight = models.IntegerField()  # 单位：g
    birthday = models.DateField()
    identity_number = models.CharField(max_length=18, validators=[validator.validate_identity_number])
    mobile = models.CharField(max_length=11, validators=[validator.validate_mobile])
    is_professional_boxer = models.BooleanField(default=False)  # True, 职业 | False，非职业
    club = models.CharField(null=True, blank=True, max_length=50)
    job = models.CharField(max_length=10)
    introduction = models.TextField(max_length=300)
    is_locked = models.BooleanField(default=False)
    experience = models.TextField(null=True, blank=True, max_length=500)
    authentication_state = models.CharField(max_length=10, default=constants.BOXER_AUTHENTICATION_STATE_WAITING,
                                            choices=constants.BOXER_AUTHENTICATION_STATE_CHOICE, )
    honor_certificate_images = StringListField(null=True)
    competition_video = models.CharField(max_length=256, null=True)
    allowed_course = StringListField(null=True, blank=True)
    refuse_reason = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'boxer_identification'


class Comment(SoftDeleteModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='+')
    ancestor = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='+')
    is_deleted = models.BooleanField(default=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comment'
        ordering = ('-created_time',)

    def reply_list(self):
        return self.__class__.objects.filter(ancestor_id=self.id).prefetch_related('user', 'parent')

    def to_user(self):
        if not self.parent.is_deleted and self.parent.id != self.ancestor_id:
            return self.parent.user


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='likes')
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'discover_like'
        unique_together = ('user', 'message',)
        ordering = ('-created_time',)


class OperationLog(models.Model):
    refer_type = models.CharField(choices=constants.OperationTarget.CHOICES, max_length=50)
    refer_pk = models.BigIntegerField()
    operator = models.ForeignKey(User, on_delete=models.deletion.PROTECT, related_name='+', db_index=False)
    operation_type = models.CharField(choices=constants.OperationType.CHOICES, max_length=50, null=True)
    operate_time = models.DateTimeField()
    content = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'operation_log'


class BoxingClub(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    avatar = models.CharField(max_length=128, default='club_avatar')
    province = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=10, null=True)
    city_index_letter = models.CharField(max_length=5, null=True)
    address = models.CharField(max_length=30)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # 经度,整数位3位-180~180
    latitude = models.DecimalField(max_digits=8, decimal_places=6)  # 纬度,整数位2位-90~90
    phone = models.CharField(max_length=11, validators=[validator.validate_mobile])
    opening_hours = models.CharField(max_length=30)
    images = StringListField()
    introduction = models.CharField(max_length=120)

    class Meta:
        db_table = 'club'


class Course(models.Model):
    boxer = models.ForeignKey(BoxerIdentification, on_delete=models.CASCADE, related_name='course')
    course_name = models.CharField(choices=constants.BOXER_ALLOWED_COURSES_CHOICE, max_length=20)
    price = models.PositiveIntegerField(null=True)  # 单位：元
    duration = models.PositiveSmallIntegerField(null=True)  # 时长，单位：min
    validity = models.DateField(null=True)  # 有效期
    orders = GenericRelation('PayOrder', related_query_name='course')
    club = models.ForeignKey(BoxingClub, on_delete=models.PROTECT, db_index=False, null=True)
    is_open = models.BooleanField(default=False)

    class Meta:
        db_table = "course"


class SmsLog(models.Model):
    mobile = models.CharField(max_length=11)
    template_code = models.CharField(max_length=30)
    content = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=512)
    business_id = models.CharField(max_length=36)

    class Meta:
        db_table = 'sms_log'
        ordering = ("-created_time",)


class BaseAuditModel(BaseModel):
    operator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+', db_index=False, null=True)

    class Meta:
        abstract = True


class HotVideo(BaseAuditModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hot_videos')
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=140)
    url = models.CharField(max_length=200)
    try_url = models.CharField(max_length=200)
    price = models.IntegerField(validators=[MinValueValidator(1)])  # 单位元
    is_show = models.BooleanField(default=True, db_index=True)
    comments = GenericRelation('Comment')
    orders = GenericRelation('PayOrder', related_query_name='hot_video')

    class Meta:
        db_table = 'hot_video'
        ordering = ("-created_time",)
        verbose_name = '热门视频'


class PayOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    status = models.SmallIntegerField(choices=constants.ORDER_PAYMENT_STATUS, default=constants.PAYMENT_STATUS_UNPAID,
                                      db_index=True)
    out_trade_no = models.BigIntegerField()
    payment_type = models.SmallIntegerField(choices=constants.PAYMENT_TYPE, null=True)
    amount = models.PositiveIntegerField()  # 单位分
    device = models.SmallIntegerField(choices=constants.DEVICE_PLATFORM)
    order_time = models.DateTimeField(auto_now_add=True)
    pay_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(null=True)  # 记录课程订单完成时间

    class Meta:
        db_table = 'pay_order'


class OrderComment(SoftDeleteModel):
    score = models.PositiveSmallIntegerField()
    content = models.TextField(max_length=300)
    images = StringListField(null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    order = models.ForeignKey(PayOrder, on_delete=models.PROTECT, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='order_comments')

    class Meta:
        db_table = 'order_comment'
        ordering = ('-created_time',)


class GameNews(BaseAuditModel):
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=50)
    views_count = models.PositiveIntegerField(default=0)
    initial_views_count = models.PositiveIntegerField(default=0)
    picture = models.CharField(max_length=200)
    stay_top = models.BooleanField(default=False)
    push_news = models.BooleanField()  # 是否推送
    start_time = models.DateTimeField(null=True)  # 推送开始时间
    end_time = models.DateTimeField(null=True)  # 推送结束时间
    app_content = models.TextField()
    share_content = models.TextField(null=True)
    comments = GenericRelation('Comment')

    class Meta:
        db_table = 'game_news'
        ordering = ('-stay_top', '-created_time',)
        verbose_name = '赛事资讯'


class Report(BaseAuditModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    reason = models.SmallIntegerField(choices=constants.REPORT_REASON_CHOICES)
    remark = models.CharField(max_length=20, null=True)
    status = models.SmallIntegerField(choices=constants.REPORT_STATUS_CHOICES,
                                      default=constants.REPORT_STATUS_NOT_PROCESSED)

    class Meta:
        db_table = 'report'
        ordering = ('-created_time',)


class Banner(BaseAuditModel):
    name = models.CharField(max_length=20)
    order_number = models.PositiveIntegerField()
    link_type = models.SmallIntegerField(choices=constants.BANNER_LINK_TYPE)
    link = models.CharField(max_length=200)
    picture = models.CharField(max_length=200)

    class Meta:
        db_table = 'banner'
        ordering = ('-order_number', '-created_time')


class WithdrawLog(BaseAuditModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="withdraw_logs")
    amount = models.PositiveIntegerField()  # unit:元
    status = models.CharField(choices=constants.WITHDRAW_STATUS_CHOICE, default=constants.WITHDRAW_STATUS_WAITING,
                              max_length=10)
    withdraw_account = models.CharField(max_length=30)
    order_number = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'withdraw_log'
        ordering = ("-created_time",)


class CourseSettleOrder(models.Model):
    order = models.ForeignKey(PayOrder, on_delete=models.PROTECT, db_index=False, related_name='+')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, db_index=False, related_name='+')
    created_time = models.DateTimeField(auto_now_add=True)
    settled = models.BooleanField(default=False)
    settled_date = models.DateField(null=True)
    settled_amount = models.PositiveIntegerField(null=True)  # 单位元

    class Meta:
        db_table = 'course_settle_order'
        ordering = ('-created_time',)

    def settle_order(self):
        self.settled = True
        self.settled_date = datetime.now()
        self.settled_amount = self.course.price
        self.save()
        # TODO 更新钱包记录
