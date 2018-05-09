# Generated by Django 2.0.4 on 2018-05-07 09:57

import biz.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0006_merge_20180504_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refer_type', models.CharField(choices=[('BOXER_IDENTIFICATION', '拳手认证')], max_length=50)),
                ('refer_pk', models.BigIntegerField()),
                ('operation_type', models.CharField(choices=[('BOXER_AUTHENTICATION_APPROVED', '拳手认证通过'), ('BOXER_AUTHENTICATION_REFUSE', '拳手认证驳回'), ('LOCK', '拳手接单状态锁定'), ('UNLOCK', '拳手接单状态解锁')], max_length=50, null=True)),
                ('operate_time', models.DateTimeField()),
                ('content', models.CharField(blank=True, max_length=100, null=True)),
                ('operator', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'operation_log',
            },
        ),
        migrations.AddField(
            model_name='boxeridentification',
            name='allowed_lessons',
            field=biz.models.StringListField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='boxeridentification',
            name='refuse_reason',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='boxeridentification',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
    ]