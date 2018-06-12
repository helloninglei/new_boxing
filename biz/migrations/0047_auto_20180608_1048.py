# Generated by Django 2.0.5 on 2018-06-08 02:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0046_merge_20180601_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=10)),
                ('course_price', models.PositiveIntegerField()),
                ('course_duration', models.IntegerField()),
                ('course_validity', models.DateField()),
                ('order_number', models.BigIntegerField()),
                ('status', models.SmallIntegerField(choices=[(1, '未支付'), (2, '待使用'), (3, '待评论'), (4, '已完成'), (5, '已过期')], db_index=True, default=1)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('pay_time', models.DateTimeField(null=True)),
                ('confirm_status', models.SmallIntegerField(choices=[(1, '未确认'), (2, '拳手已确认'), (3, '用户已确认')], default=1)),
                ('boxer_confirm_time', models.DateTimeField(null=True)),
                ('user_confirm_time', models.DateTimeField(null=True)),
                ('finish_time', models.DateTimeField(null=True)),
                ('amount', models.PositiveIntegerField(null=True)),
                ('boxer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='boxer_course_order', to='biz.BoxerIdentification')),
                ('club', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.PROTECT, to='biz.BoxingClub')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='course_orders', to='biz.Course')),
                ('pay_order', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='business_order', to='biz.PayOrder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_course_order', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'course_order',
                'ordering': ('-created_time',),
            },
        ),
        migrations.AlterField(
            model_name='ordercomment',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comment', to='biz.CourseOrder'),
        ),
    ]
