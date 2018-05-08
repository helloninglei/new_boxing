# Generated by Django 2.0.4 on 2018-04-27 10:00

import biz.validator
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0003_auto_20180425_2013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('-created_time',)},
        ),
        migrations.AlterField(
            model_name='coinchangelog',
            name='change_type',
            field=models.CharField(choices=[('INCREASE_COIN_RECHARGE', '收入-充值'), ('INCREASE_COIN_OFFICIAL_RECHARGE', '官方充值'), ('INCREASE_GUESSING_AWARD', '竞猜奖励'), ('INCREASE_USER_DONATE', '收入-用户打赏'), ('INCREASE_USER_VIDEO_DONATE', '收入-用户视频打赏'), ('INCREASE_COIN_REJECT_WITHDRAW_REBACK', '提现被拒绝-退回款项'), ('INCREASE_WITHDRAW_FAILED_REBACK', '提现失败-退回款项'), ('REDUCE_USER_DONATE', '支出-用户打赏'), ('REDUCE_USER_VIDEO_DONATE', '支出-用户视频打赏'), ('REDUCE_SHOPPING_EXCHANGE', '商城兑换'), ('REDUCE_GUESSING_BET', '竞猜下注'), ('REDUCE_START_VOTE', '支出明星投票'), ('REDUCE_WITHDRAW_APPLY', '提现申请提现')], max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='moneychangelog',
            name='change_type',
            field=models.CharField(choices=[('INCREASE_MONEY_RECHARGE', '充值'), ('INCREASE_MONEY_OFFICIAL_RECHARGE', '官方充值'), ('INCREASE_ORDER', '约单(收入)'), ('INCREASE_MONEY_REJECT_WITHDRAW_REBACK', '提现(审核未通过)'), ('REDUCE_WITHDRAW', '提现'), ('REDUCE_ORDER', '约单(支出)'), ('REDUCE_PAY_FOR_VIDEO', '付费视频'), ('REDUCE_SIGN_UP', '报名')], max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(db_index=True, error_messages={'unique': '手机号已存在。'}, max_length=11, unique=True, validators=[biz.validator.validate_mobile]),
        ),
    ]
