# Generated by Django 2.0.5 on 2018-05-22 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0024_merge_20180522_1358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('-created_time',), 'verbose_name': '动态'},
        ),
        migrations.AddField(
            model_name='course',
            name='is_open',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='boxeridentification',
            name='competition_video',
            field=models.CharField(max_length=256, null=True),
        ),
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