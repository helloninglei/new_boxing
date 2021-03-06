# Generated by Django 2.0.4 on 2018-05-04 02:36

import biz.models
import biz.validator
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0004_auto_20180427_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoxerIdentification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('real_name', models.CharField(max_length=10)),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('birthday', models.DateField()),
                ('identity_number', models.CharField(max_length=18, validators=[biz.validator.validate_identity_number])),
                ('mobile', models.CharField(max_length=11, validators=[biz.validator.validate_mobile])),
                ('is_professional_boxer', models.BooleanField(default=False)),
                ('club', models.CharField(blank=True, max_length=50, null=True)),
                ('job', models.CharField(max_length=10)),
                ('introduction', models.TextField(max_length=300)),
                ('experience', models.TextField(blank=True, max_length=500, null=True)),
                ('authentication_state', models.CharField(choices=[('WAITING', '待审核'), ('REFUSE', '已驳回'), ('APPROVED', '已通过')], default='WAITING', max_length=10)),
                ('is_locked', models.BooleanField(default=True)),
                ('honor_certificate_images', biz.models.StringListField(null=True)),
                ('competition_video', models.URLField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='boxer_identification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'boxer_identification',
            },
        ),
        migrations.AlterField(
            model_name='coinchangelog',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='moneychangelog',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
