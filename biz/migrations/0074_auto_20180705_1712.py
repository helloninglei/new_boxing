# Generated by Django 2.0.6 on 2018-07-05 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0073_wordfilter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordfilter',
            name='sensitive_word',
            field=models.CharField(db_index=True, max_length=20, unique=True),
        ),
    ]
