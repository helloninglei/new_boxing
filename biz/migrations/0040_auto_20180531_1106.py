# Generated by Django 2.0.5 on 2018-05-31 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0039_merge_20180530_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='remark',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]