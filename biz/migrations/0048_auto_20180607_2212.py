# Generated by Django 2.0.5 on 2018-06-07 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0047_auto_20180607_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorder',
            name='order_number',
            field=models.BigIntegerField(),
        ),
    ]
