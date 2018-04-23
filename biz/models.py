# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from constants import DISCOVER_MEDIA
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BaseModel(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+', null=True)
    created_time = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AuditModel(BaseModel):
    approver = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='+', blank=True)
    approved_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


# 动态
class Thread(BaseModel):
    content = models.CharField(max_length=140)
    is_deleted = models.BooleanField(default=False, db_index=True)

    def author_id(self):
        return self.creator.id

# 图片视频
class Media(BaseModel):
    thread = models.ForeignKey(Thread, on_delete=models.PROTECT, null=True, related_name='medias')
    url = models.CharField(max_length=255)
    media_type = models.SmallIntegerField(choices=DISCOVER_MEDIA.CHOICES, db_index=True)