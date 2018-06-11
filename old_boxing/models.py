from django.db import models


class Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('old_boxing')


class Article(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=30)
    subtitle = models.CharField(db_column='subTitle', max_length=80)  # Field name made lowercase.
    author = models.CharField(max_length=20)
    basereadnum = models.IntegerField(db_column='baseReadNum')  # Field name made lowercase.
    realreadnum = models.IntegerField(db_column='realReadNum')  # Field name made lowercase.
    readpersonnum = models.IntegerField(db_column='readPersonNum')  # Field name made lowercase.
    cover = models.CharField(max_length=100)
    contenttype = models.IntegerField(db_column='contentType')  # Field name made lowercase.
    istotop = models.IntegerField(db_column='isToTop')  # Field name made lowercase.
    contenthtml = models.TextField(db_column='contentHtml')  # Field name made lowercase.
    share_content_html = models.TextField(blank=True, null=True)
    favoritetimes = models.IntegerField(db_column='favoriteTimes', blank=True, null=True)  # Field name made lowercase.
    hasrecommend = models.IntegerField(db_column='hasRecommend', blank=True, null=True)  # Field name made lowercase.
    sharetimes = models.IntegerField(db_column='shareTimes', blank=True, null=True)  # Field name made lowercase.
    isdel = models.IntegerField(db_column='isDel')  # Field name made lowercase.
    is_push = models.IntegerField(blank=True, null=True)
    push_start_time = models.DateTimeField(blank=True, null=True)
    push_end_time = models.DateTimeField(blank=True, null=True)
    createtime = models.DateTimeField(db_column='createTime', blank=True, null=True)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='updateTime', blank=True, null=True)  # Field name made lowercase.
    targetid = models.BigIntegerField(db_column='targetId', blank=True, null=True)  # Field name made lowercase.

    objects = Manager()

    class Meta:
        managed = False
        db_table = 'article'
        unique_together = (('id', 'contenttype'),)


class ArticleComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    aid = models.BigIntegerField()
    uid = models.BigIntegerField()
    content = models.CharField(max_length=255)
    isdel = models.IntegerField(db_column='isDel', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='createTime', blank=True, null=True)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='updateTime', blank=True, null=True)  # Field name made lowercase.

    objects = Manager()

    class Meta:
        managed = False
        db_table = 'article_comment'


class User(models.Model):
    uid = models.BigAutoField(primary_key=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    nickname = models.CharField(db_column='nickName', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    gender = models.IntegerField(blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    pass_field = models.CharField(db_column='pass', max_length=60, blank=True,
                                  null=True)  # Field renamed because it was a Python reserved word.
    salt = models.CharField(max_length=50, blank=True, null=True)
    signature = models.CharField(max_length=100, blank=True, null=True)
    summary = models.CharField(max_length=255, blank=True, null=True)
    city = models.IntegerField(blank=True, null=True)
    photos = models.CharField(max_length=500, blank=True, null=True)
    bgavatar = models.CharField(db_column='bgAvatar', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    uicon = models.CharField(max_length=512, blank=True, null=True)
    avatar = models.CharField(max_length=512, blank=True, null=True)
    praisetimes = models.IntegerField(db_column='praiseTimes', blank=True, null=True)  # Field name made lowercase.
    favoritetimes = models.IntegerField(db_column='favoriteTimes', blank=True, null=True)  # Field name made lowercase.
    rewardtimes = models.IntegerField(db_column='rewardTimes', blank=True, null=True)  # Field name made lowercase.
    activevalue = models.IntegerField(db_column='activeValue', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    geohash = models.CharField(max_length=32, blank=True, null=True)
    token = models.CharField(max_length=64, blank=True, null=True)
    uuid = models.CharField(max_length=100, blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)
    isonline = models.IntegerField(db_column='isOnline', blank=True, null=True)  # Field name made lowercase.
    isdel = models.IntegerField(db_column='isDel', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='createTime', blank=True, null=True)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='updateTime', blank=True, null=True)  # Field name made lowercase.
    rewardtotalmoney = models.BigIntegerField(db_column='rewardTotalMoney', blank=True,
                                              null=True)  # Field name made lowercase.
    objects = Manager()

    class Meta:
        managed = False
        db_table = 'user'


class UserInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.BigIntegerField()
    gender = models.IntegerField()
    name = models.CharField(max_length=100)
    avatar = models.CharField(max_length=150)
    stature = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    birthday = models.DateTimeField()
    idcard = models.CharField(db_column='idCard', max_length=20)  # Field name made lowercase.
    phone = models.CharField(max_length=20)
    occupation = models.CharField(max_length=20)
    club = models.CharField(max_length=20)
    playertype = models.IntegerField(db_column='playerType')  # Field name made lowercase.
    updateweighttime = models.DateTimeField(db_column='updateWeightTime')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='createTime')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='updateTime')  # Field name made lowercase.

    objects = Manager()

    class Meta:
        managed = False
        db_table = 'user_info'
