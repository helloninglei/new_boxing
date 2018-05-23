from celery import shared_task
from biz.easemob_client import EaseMobClient


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def register_easemob_account(*usernames):
    EaseMobClient.batch_register(*usernames)
