# Generated by Django 2.0.5 on 2018-05-21 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0022_merge_20180521_1204'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gamenews',
            options={'ordering': ('-stay_top', '-created_time')},
        ),
        migrations.RenameField(
            model_name='boxeridentification',
            old_name='allowed_lessons',
            new_name='allowed_course',
        ),
        migrations.AlterField(
            model_name='course',
            name='duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='validity',
            field=models.DateField(null=True),
        ),
    ]
