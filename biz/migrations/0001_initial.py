# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-19 06:54
from __future__ import unicode_literals

import biz.models
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('mobile', models.CharField(db_index=True, max_length=11, unique=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('weibo_openid', models.CharField(blank=True, max_length=128, null=True, unique=True)),
                ('wechat_openid', models.CharField(blank=True, max_length=128, null=True, unique=True)),
                ('coin_balance', models.IntegerField(default=0)),
                ('money_balance', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'db_table': 'user',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', biz.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BoxerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('audit_time', models.DateTimeField()),
                ('identity_number', models.CharField(max_length=18)),
                ('mobile', models.CharField(max_length=11)),
                ('is_professional_boxer', models.BooleanField(default=False)),
                ('club', models.CharField(max_length=128)),
                ('introduction', models.TextField()),
                ('auditor', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='boxer_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'boxer_profile',
            },
        ),
        migrations.CreateModel(
            name='BoxerProfileAdditional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('data_url', models.URLField()),
                ('data_type', models.CharField(choices=[('IMAGE', '\u56fe\u7247'), ('VIDEO', '\u89c6\u9891')], max_length=30)),
                ('boxer_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boxer_profile_additional', to='biz.BoxerProfile')),
            ],
            options={
                'db_table': 'boxer_profile_additional',
            },
        ),
        migrations.CreateModel(
            name='UserBalanceBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('audit_time', models.DateTimeField()),
                ('balance_type', models.CharField(choices=[('BOXING_BEAN', '\u62f3\u8c46'), ('WALLET', '\u94b1\u5305')], max_length=10)),
                ('balance_bill_type', models.CharField(choices=[('CHARGE', '\u5145\u503c'), ('APPOINTMENT', '\u7ea6\u5355'), ('REGISTERED', '\u62a5\u540d'), ('PAY_VIDEO', '\u4ed8\u8d39\u89c6\u9891'), ('CONVERT_BOXING_BEANS', '\u5151\u6362\u62f3\u8c46'), ('WITH_DRAW', '\u63d0\u73b0')], max_length=10)),
                ('amount', models.IntegerField()),
                ('remark', models.CharField(blank=True, max_length=30, null=True)),
                ('auditor', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_balance_bill', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_balance_bill',
            },
        ),
        migrations.CreateModel(
            name='UserPaymentBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('trade_amount', models.IntegerField()),
                ('order_id', models.CharField(max_length=128)),
                ('trade_device', models.CharField(choices=[('IOS', 'ios'), ('ANDROID', 'Android')], max_length=10)),
                ('trade_channel', models.CharField(choices=[('ALIPAY', '\u652f\u4ed8\u5b9d'), ('WEIXIN', '\u5fae\u4fe1'), ('WALLET', '\u94b1\u5305')], max_length=10)),
                ('status', models.CharField(choices=[('SUCCESS', '\u652f\u4ed8\u6210\u529f'), ('FAIL', '\u652f\u4ed8\u5931\u8d25'), ('UNCOMPLETED', '\u652f\u4ed8\u672a\u5b8c\u6210')], max_length=10)),
                ('remark', models.CharField(blank=True, max_length=50, null=True)),
                ('bill_type', models.CharField(choices=[('CHARGE', '\u5145\u503c'), ('APPOINTMENT', '\u7ea6\u5355'), ('REGISTERED', '\u62a5\u540d'), ('PAY_VIDEO', '\u4ed8\u8d39\u89c6\u9891'), ('CONVERT_BOXING_BEANS', '\u5151\u6362\u62f3\u8c46')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_payment_bills', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_payment_bill',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('nick_name', models.CharField(max_length=30)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('nation', models.CharField(blank=True, max_length=30, null=True)),
                ('birthday', models.DateTimeField(blank=True, null=True)),
                ('weight', models.CharField(blank=True, max_length=10, null=True)),
                ('height', models.CharField(blank=True, max_length=10, null=True)),
                ('profession', models.CharField(blank=True, max_length=20, null=True)),
                ('avatar', models.URLField(blank=True, null=True)),
                ('gender', models.BooleanField(default=True)),
                ('address', models.CharField(blank=True, max_length=254, null=True)),
                ('bio', models.CharField(blank=True, max_length=30, null=True)),
                ('alipay_account', models.CharField(blank=True, max_length=30, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
        migrations.CreateModel(
            name='UserRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('is_friend', models.BooleanField(default=False)),
                ('is_black', models.BooleanField(default=False)),
                ('is_follower', models.BooleanField(default=False)),
                ('passive_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followings', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_relation',
            },
        ),
        migrations.CreateModel(
            name='UserWithDrawApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('audit_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('WAITING', '\u5f85\u5ba1\u6838'), ('APPROVE', '\u901a\u8fc7'), ('REJECT', '\u9a73\u56de')], max_length=50)),
                ('amount', models.IntegerField()),
                ('channel', models.CharField(choices=[('ALIPAY', '\u652f\u4ed8\u5b9d'), ('WEIXIN', '\u5fae\u4fe1')], max_length=10)),
                ('receivable_account', models.CharField(max_length=50)),
                ('auditor', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_with_draw_applications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_with_draw_application',
            },
        ),
    ]
