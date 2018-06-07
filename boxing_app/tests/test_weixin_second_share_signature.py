from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase


class WeiXinSecondShareSignatureTestCase(APITestCase):
    def setUp(self):
        self.client = self.client_class()

    @patch("biz.weixin_public_client.WeiXinPublicPlatformClient.fetch_jsapi_ticket")
    def test(self, jsapi_ticket):
        ticket = "HoagFKDcsGMVCIY2vOjf9hPsrxNEwtaswZk2RxVPA8C7pxSezYLGujzXi13S7PyBDCM2rKfz1HrpGEXbkfTJQw"
        jsapi_ticket.return_value = ticket

        response = self.client.get(path="/second_share_signature")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['jsapi_ticket'], ticket)
        self.assertIsNone(response.data['url'])
