# Generated by Django 2.0.5 on 2018-05-24 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0030_auto_20180523_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payorder',
            name='payment_type',
            field=models.SmallIntegerField(choices=[(1, '支付宝'), (2, '微信'), (3, '余额')], null=True),
        ),
    ]
