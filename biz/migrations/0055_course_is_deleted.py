# Generated by Django 2.0.5 on 2018-06-10 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0054_courseorder_insurance_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]