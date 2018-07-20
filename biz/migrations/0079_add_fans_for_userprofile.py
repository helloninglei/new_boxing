from django.db import migrations

from biz import redis_client


def update_user_fans_count(apps, schema_editor):
    UserProfile = apps.get_model("biz", "UserProfile")
    key_list = redis_client.redis_client.keys(pattern='follower_*')
    for key in key_list:
        user_id = int(key.split('_')[1])
        follower_count = redis_client.redis_client.zcard(key)
        UserProfile.objects.filter(id=user_id).update(fans=follower_count)


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0078_userprofile_fans'),
    ]

    operations = [
        migrations.RunPython(update_user_fans_count)
    ]
