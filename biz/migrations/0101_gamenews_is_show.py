# Generated by Django 2.0.8 on 2018-10-12 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0100_auto_20181011_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamenews',
            name='is_show',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
