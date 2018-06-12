# Generated by Django 2.0.5 on 2018-06-12 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0058_merge_20180612_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorder',
            name='refund_record',
            field=models.ForeignKey(db_index=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='biz.MoneyChangeLog'),
        ),
        migrations.AlterField(
            model_name='moneychangelog',
            name='change_type',
            field=models.CharField(choices=[('INCREASE_MONEY_RECHARGE', '充值'), ('INCREASE_MONEY_OFFICIAL_RECHARGE', '官方充值'), ('INCREASE_ORDER', '约单(收入)'), ('INCREASE_ORDER_OVERDUE', '约单(过期)'), ('INCREASE_MONEY_REJECT_WITHDRAW_REBACK', '提现(审核未通过)'), ('REDUCE_WITHDRAW', '提现'), ('REDUCE_ORDER', '约单(支出)'), ('REDUCE_PAY_FOR_VIDEO', '付费视频'), ('REDUCE_SIGN_UP', '报名')], max_length=64, null=True),
        ),
    ]