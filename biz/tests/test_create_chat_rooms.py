from unittest.mock import patch
from biz.easemob_client import EaseMobClient
from rest_framework.test import APITestCase
from django.core.management import call_command
from biz.constants import SERVICE_USER_ID, CHAT_ROOM_NAME, CHAT_ROOM_DESCRIPTION
from biz.redis_client import redis_client
from biz.redis_const import EASEMOB_CHAT_ROOMS_INFO


class CreateChatRoomsCommandTestCase(APITestCase):

    @patch("biz.easemob_client.EaseMobClient.create_chatrooms")
    def test_create_chatrooms(self, create_chatrooms):
        self.assertIs(EaseMobClient.create_chatrooms, create_chatrooms)
        create_chatrooms.return_value = "success"
        redis_client.set(EASEMOB_CHAT_ROOMS_INFO, "value")
        self.assertTrue(redis_client.exists(EASEMOB_CHAT_ROOMS_INFO))
        call_command("create_chatrooms")
        create_chatrooms.assert_called()
        create_chatrooms.assert_called_with(CHAT_ROOM_NAME, CHAT_ROOM_DESCRIPTION, str(SERVICE_USER_ID))
        self.assertFalse(redis_client.exists(EASEMOB_CHAT_ROOMS_INFO))
