# Created by fzw on 2018-06-27
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [('biz', '0067_auto_20180627_1725')]

    operations = [
        migrations.RunSQL("update user set user_type = 1 where user.id in (select boxer.user_id from boxer_identification boxer where boxer.authentication_state = 'APPROVED');")
    ]
