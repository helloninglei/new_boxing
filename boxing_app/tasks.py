from celery import shared_task
from django.db.models import F
from biz.easemob_client import EaseMobClient
from biz.constants import SERVICE_USER_ID
from biz.models import HotVideo


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def register_easemob_account(*usernames):
    EaseMobClient.batch_register(*usernames)
    msg = "欢迎来到拳城出击！"
    return EaseMobClient.send_text_messages(msg, SERVICE_USER_ID, *usernames)


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def set_hot_video_like_count(video_id, count):
    HotVideo.objects.filter(pk=video_id).update(like_count=count)


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def incr_hot_video_views_count(video_id):
    HotVideo.objects.filter(pk=video_id).update(views_count=F('views_count') + 1)
