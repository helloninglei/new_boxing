# Generated by Django 2.0.5 on 2018-05-22 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0024_merge_20180522_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='duration',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
