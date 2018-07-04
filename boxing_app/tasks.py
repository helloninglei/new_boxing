import biz.management.commands.migrate_data

from celery import shared_task
from biz.easemob_client import EaseMobClient
from biz.constants import SERVICE_USER_ID


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def register_easemob_account(*usernames):
    EaseMobClient.batch_register(*usernames)
    msg = "欢迎来到拳城出击！"
    return EaseMobClient.send_text_messages(msg, SERVICE_USER_ID, *usernames)
