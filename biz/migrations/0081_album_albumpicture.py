# Generated by Django 2.0.7 on 2018-08-31 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0080_merge_20180725_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32)),
                ('release_time', models.DateTimeField()),
                ('is_show', models.BooleanField()),
                ('related_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '相册',
                'db_table': 'album',
                'ordering': ('-created_time',),
            },
        ),
        migrations.CreateModel(
            name='AlbumPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.CharField(max_length=200)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='biz.Album')),
            ],
            options={
                'db_table': 'picture',
                'ordering': ('-created_time',),
            },
        ),
    ]
