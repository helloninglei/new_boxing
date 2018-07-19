from django.db import migrations

from biz import redis_client


def create_users_set_order_by_follower(apps, schema_editor):
    key_list = redis_client.redis_client.keys(pattern='follower_*')
    p = redis_client.redis_client.pipeline()
    for key in key_list:
        user_id = int(key.split('_')[1])
        follower_count = redis_client.follower_count(user_id)
        p.zadd('users_by_follower', user_id=follower_count)
    p.execute()


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0077_auto_20180712_1556'),
    ]

    operations = [
        migrations.RunPython(create_users_set_order_by_follower)
    ]
