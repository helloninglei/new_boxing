from celery import shared_task
from biz.easemob_client import EaseMobClient
from biz.constants import SERVICE_USER_ID
from biz.models import UserProfile


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def register_easemob_account(*usernames):
    EaseMobClient.batch_register(*usernames)
    user = UserProfile.objects.get(user_id=SERVICE_USER_ID)
    msg = "欢迎来到拳城出击！"
    resp = EaseMobClient.send_text_messages(msg, SERVICE_USER_ID, user.nick_name, user.avatar, usernames)
    print(resp)
    return resp
