# Generated by Django 2.0.8 on 2018-09-13 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0084_auto_20180905_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='hotvideo',
            name='tag',
            field=models.PositiveSmallIntegerField(choices=[(1, '徐晓冬'), (2, '冬哥辣评'), (3, '拳城出击'), (4, '教学'), (5, '街斗'), (6, '搞笑'), (7, '美女'), (8, '国外'), (9, '热点')], default=3),
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name='ordercomment',
            name='content',
            field=models.CharField(max_length=300),
        ),
    ]
