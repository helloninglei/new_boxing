# Generated by Django 2.0.7 on 2018-07-12 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0076_migrate_hot_video_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotvideo',
            options={'ordering': ('stay_top', '-created_time'), 'verbose_name': '热门视频'},
        ),
        migrations.AddField(
            model_name='hotvideo',
            name='stay_top',
            field=models.BooleanField(default=False),
        ),
    ]
