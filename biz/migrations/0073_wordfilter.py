# Generated by Django 2.0.6 on 2018-07-05 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0072_merge_20180705_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('sensitive_word', models.CharField(db_index=True, max_length=20)),
            ],
            options={
                'db_table': 'word_filter',
                'ordering': ('-updated_time',),
            },
        ),
    ]