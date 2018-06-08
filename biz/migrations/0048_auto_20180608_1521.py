# Generated by Django 2.0.5 on 2018-06-08 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0047_auto_20180608_1048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseorder',
            options={'ordering': ('-order_time',)},
        ),
        migrations.RemoveField(
            model_name='courseorder',
            name='settle_time',
        ),
        migrations.AlterField(
            model_name='courseorder',
            name='pay_order',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='business_order', to='biz.PayOrder'),
        ),
        migrations.AlterModelTable(
            name='courseorder',
            table='course_order',
        ),
    ]
