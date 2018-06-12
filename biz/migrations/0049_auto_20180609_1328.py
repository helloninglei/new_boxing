# Generated by Django 2.0.6 on 2018-06-09 05:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0048_auto_20180606_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_time',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='gamenews',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]