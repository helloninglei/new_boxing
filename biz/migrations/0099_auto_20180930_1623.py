# Generated by Django 2.0.8 on 2018-09-30 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0098_auto_20180926_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='content',
            field=models.TextField(max_length=500),
        ),
    ]
