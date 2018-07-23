from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase
from biz.models import WordFilter


class ChatRoomsInfoTestCase(APITestCase):
    def setUp(self):
        self.client = self.client_class()

    @patch("biz.easemob_client.EaseMobClient.get_chatrooms")
    def test_chat_rooms_info(self, get_chatrooms):
        chat_rooms_info = [
            {
                "id": "53878933487617",
                "name": "拳城BB",
                "owner": "13",
                "affiliations_count": 1
            },
            {
                "id": "53875094650881",
                "name": "拳城BB",
                "owner": "13",
                "affiliations_count": 1
            }
        ]
        get_chatrooms.return_value = chat_rooms_info
        WordFilter.objects.bulk_create([WordFilter(sensitive_word=f"{i}") for i in range(2)])
        response = self.client.get(path="/chat_rooms_info")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data['chat_rooms_info'], chat_rooms_info)
        self.assertListEqual(list(response.data['sensitive_word_list']),
                             list(WordFilter.objects.values_list("sensitive_word", flat=True)))
