# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-23 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0002_auto_20180423_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='coin_balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='money_balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='coinchangelog',
            name='change_type',
            field=models.CharField(choices=[(b'INCREASE_COIN_RECHARGE', '\u6536\u5165-\u5145\u503c'), (b'INCREASE_COIN_OFFICIAL_RECHARGE', '\u5b98\u65b9\u5145\u503c'), (b'INCREASE_GUESSING_AWARD', '\u7ade\u731c\u5956\u52b1'), (b'INCREASE_USER_DONATE', '\u6536\u5165-\u7528\u6237\u6253\u8d4f'), (b'INCREASE_USER_VIDEO_DONATE', '\u6536\u5165-\u7528\u6237\u89c6\u9891\u6253\u8d4f'), (b'INCREASE_COIN_REJECT_WITHDRAW_REBACK', '\u63d0\u73b0\u88ab\u62d2\u7edd-\u9000\u56de\u6b3e\u9879'), (b'INCREASE_WITHDRAW_FAILED_REBACK', '\u63d0\u73b0\u5931\u8d25-\u9000\u56de\u6b3e\u9879'), (b'REDUCE_USER_DONATE', '\u652f\u51fa-\u7528\u6237\u6253\u8d4f'), (b'REDUCE_USER_VIDEO_DONATE', '\u652f\u51fa-\u7528\u6237\u89c6\u9891\u6253\u8d4f'), (b'REDUCE_SHOPPING_EXCHANGE', '\u5546\u57ce\u5151\u6362'), (b'REDUCE_GUESSING_BET', '\u7ade\u731c\u4e0b\u6ce8'), (b'REDUCE_START_VOTE', '\u652f\u51fa\u660e\u661f\u6295\u7968'), (b'REDUCE_WITHDRAW_APPLY', '\u63d0\u73b0\u7533\u8bf7\u63d0\u73b0')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='moneychangelog',
            name='change_type',
            field=models.CharField(choices=[(b'INCREASE_COIN_RECHARGE', '\u6536\u5165-\u5145\u503c'), (b'INCREASE_COIN_OFFICIAL_RECHARGE', '\u5b98\u65b9\u5145\u503c'), (b'INCREASE_GUESSING_AWARD', '\u7ade\u731c\u5956\u52b1'), (b'INCREASE_USER_DONATE', '\u6536\u5165-\u7528\u6237\u6253\u8d4f'), (b'INCREASE_USER_VIDEO_DONATE', '\u6536\u5165-\u7528\u6237\u89c6\u9891\u6253\u8d4f'), (b'INCREASE_COIN_REJECT_WITHDRAW_REBACK', '\u63d0\u73b0\u88ab\u62d2\u7edd-\u9000\u56de\u6b3e\u9879'), (b'INCREASE_WITHDRAW_FAILED_REBACK', '\u63d0\u73b0\u5931\u8d25-\u9000\u56de\u6b3e\u9879'), (b'REDUCE_USER_DONATE', '\u652f\u51fa-\u7528\u6237\u6253\u8d4f'), (b'REDUCE_USER_VIDEO_DONATE', '\u652f\u51fa-\u7528\u6237\u89c6\u9891\u6253\u8d4f'), (b'REDUCE_SHOPPING_EXCHANGE', '\u5546\u57ce\u5151\u6362'), (b'REDUCE_GUESSING_BET', '\u7ade\u731c\u4e0b\u6ce8'), (b'REDUCE_START_VOTE', '\u652f\u51fa\u660e\u661f\u6295\u7968'), (b'REDUCE_WITHDRAW_APPLY', '\u63d0\u73b0\u7533\u8bf7\u63d0\u73b0')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
