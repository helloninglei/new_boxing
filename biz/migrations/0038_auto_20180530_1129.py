# Generated by Django 2.0.5 on 2018-05-30 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0037_merge_20180529_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxingclub',
            name='avatar',
            field=models.CharField(default='club_avatar', max_length=128),
        ),
        migrations.AddField(
            model_name='boxingclub',
            name='city',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='boxingclub',
            name='province',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
