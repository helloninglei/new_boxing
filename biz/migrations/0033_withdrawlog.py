# Generated by Django 2.0.5 on 2018-05-28 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0032_merge_20180525_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('WAITING', '审核中'), ('APPROVED', '审核通过'), ('REJECTED', '审核未通过')], default='WAITING', max_length=10)),
                ('withdraw_account', models.CharField(max_length=20)),
                ('order_number', models.CharField(max_length=50, unique=True)),
                ('operator', models.ForeignKey(db_index=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdraw_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'withdraw_log',
                'ordering': ('-created_time',),
            },
        ),
    ]