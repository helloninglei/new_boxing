# Generated by Django 2.0.7 on 2018-10-10 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0089_merge_20180926_1725'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appversion',
            options={'ordering': ('-created_time',)},
        ),
    ]