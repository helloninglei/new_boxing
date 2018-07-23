# Generated by Django 2.0.5 on 2018-06-27 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0066_auto_20180627_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='title',
            field=models.CharField(blank=True, max_length=56, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(blank=True, choices=[(1, '拳手'), (2, '名人'), (3, '自媒体')], null=True),
        ),
    ]
