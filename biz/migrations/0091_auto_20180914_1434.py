# Generated by Django 2.0.7 on 2018-09-14 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0090_merge_20180914_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='level',
        ),
        migrations.AddField(
            model_name='match',
            name='level_max',
            field=models.IntegerField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='level_min',
            field=models.IntegerField(),
            preserve_default=False,
        ),
    ]
