# Generated by Django 2.0.8 on 2018-10-30 10:26

from django.db import migrations


def alter_user_real_name_to_boxer_real_name(apps, schema_editor):
    BoxerIdentification = apps.get_model('biz', 'BoxerIdentification')
    UserProfile = apps.get_model('biz', 'UserProfile')
    boxers = BoxerIdentification.objects.all()
    for boxer in boxers:
        if boxer.real_name:
            UserProfile.objects.filter(user=boxer.user).update(name=boxer.real_name)


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0105_auto_20181022_1006'),
    ]

    operations = [
        migrations.RunPython(alter_user_real_name_to_boxer_real_name),

    ]
