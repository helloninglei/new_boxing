# Generated by Django 2.0.8 on 2018-10-22 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0104_auto_20181015_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxeridentification',
            name='job',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profession',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]