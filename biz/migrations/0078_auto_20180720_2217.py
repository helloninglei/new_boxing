# Generated by Django 2.0.6 on 2018-07-20 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0077_auto_20180712_1556'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotvideo',
            options={'ordering': ('-stay_top', '-created_time'), 'verbose_name': '热门视频'},
        ),
    ]
