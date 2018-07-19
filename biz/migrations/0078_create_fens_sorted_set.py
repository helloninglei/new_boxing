from django.db import migrations

from biz import redis_client


def init_user_set(apps, schema_editor):
    p = redis_client.redis_client.pipeline()
    User = apps.get_model("biz", "User")
    id_list = User.objects.all().values_list('id', flat=True)
    [p.zadd('user_set_order_by_follower', 0, id) for id in id_list]
    p.execute()


def update_user_set_follower_count(apps, schema_editor):
    key_list = redis_client.redis_client.keys(pattern='follower_*')
    p = redis_client.redis_client.pipeline()
    for key in key_list:
        user_id = int(key.split('_')[1])
        follower_count = redis_client.follower_count(user_id)
        p.zadd('user_set_order_by_follower', follower_count, user_id)
    p.execute()


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0077_auto_20180712_1556'),
    ]

    operations = [
        migrations.RunPython(init_user_set),
        migrations.RunPython(update_user_set_follower_count)
    ]
