# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
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

class StringListField(models.TextField):
    def prepare_value(self, value):
        return json.dumps(value)

    def to_python(self, value):
        if not value:
            return []
        return json.loads(value)

class ThreadManager(models.Manager):
    def get_queryset(self):
        return super(ThreadManager, self).get_queryset().filter(is_deleted=False)

# 动态
class Thread(BaseModel):
    content = models.CharField(max_length=140)
    images = StringListField()
    video = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False, db_index=True)

    objects = ThreadManager()

    class Meta:
        db_table = 'discover_thread'