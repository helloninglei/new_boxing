# Generated by Django 2.0.4 on 2018-05-09 08:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0011_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=140)),
                ('url', models.URLField()),
                ('try_url', models.URLField()),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('is_show', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hot_videos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HotVideoOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(1, '未支付'), (2, '已支付')], db_index=True, default=1)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('pay_time', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='biz.HotVideo')),
            ],
        ),
    ]
