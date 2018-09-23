# Generated by Django 2.0.7 on 2018-09-22 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from biz.constants import APPVERSION_NOW, ANDROID, IOS


def make_init_app_version(apps, schema_editor):
    AppVersion = apps.get_model("biz", "AppVersion")
    AppVersion.objects.create(version='3.3.0', platform=ANDROID, status=APPVERSION_NOW, message='version:3.3.0', force=True,
                              inner_number=44, package='/path/to/file.apk')
    AppVersion.objects.create(version='3.3.0', platform=IOS, status=APPVERSION_NOW, message='version:3.3.0', force=True,
                              inner_number=0, package='')


class Migration(migrations.Migration):
    dependencies = [
        ('biz', '0086_merge_20180914_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('version', models.CharField(max_length=16)),
                ('platform', models.CharField(choices=[('android', '安卓'), ('ios', 'IOS')], max_length=16)),
                ('status', models.CharField(choices=[('PAST', '历史版本'), ('NOW', '当前版本'), ('FUTURE', '未上线')], max_length=16)),
                ('message', models.CharField(max_length=1024)),
                ('inner_number', models.IntegerField(blank=True, null=True)),
                ('force', models.BooleanField()),
                ('package', models.CharField(blank=True, max_length=256, null=True)),
                ('operator', models.ForeignKey(db_index=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+',
                                               to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'app_version',
                'ordering': ('-updated_time',),
            },
        ),
        migrations.AddIndex(
            model_name='appversion',
            index=models.Index(fields=['platform', 'status'], name='app_version_platfor_09b0c9_idx'),
        ),
        migrations.RunPython(make_init_app_version)
    ]
