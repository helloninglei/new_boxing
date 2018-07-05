from django.core.management.base import BaseCommand
from biz.constants import SERVICE_USER_ID, CHAT_ROOM_NAME, CHAT_ROOM_DESCRIPTION
from biz.easemob_client import EaseMobClient
from biz.redis_client import redis_client
from biz.redis_const import EASEMOB_CHAT_ROOMS_INFO


class Command(BaseCommand):
    help = "创建聊天室"

    def handle(self, *args, **options):
        EaseMobClient.create_chatrooms(CHAT_ROOM_NAME, CHAT_ROOM_DESCRIPTION, str(SERVICE_USER_ID))
        redis_client.delete(EASEMOB_CHAT_ROOMS_INFO)
