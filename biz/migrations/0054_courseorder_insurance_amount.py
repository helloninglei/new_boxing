# Generated by Django 2.0.5 on 2018-06-10 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0053_auto_20180610_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorder',
            name='insurance_amount',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
