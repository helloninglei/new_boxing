# Generated by Django 2.0.8 on 2018-09-03 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0081_merge_20180903_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotvideo',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='hotvideo',
            name='push_hot_video',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='hotvideo',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='hotvideo',
            name='tag',
            field=models.PositiveSmallIntegerField(
                choices=[(1, '拳城出击'), (2, '徐晓冬'), (3, '教学'), (4, '街斗'), (5, '搞笑'), (6, '美女'), (7, '国外'), (8, '热点')],
                default=1),
        ),
    ]