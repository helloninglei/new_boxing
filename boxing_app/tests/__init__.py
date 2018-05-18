from rest_framework.test import APITestCase
from biz import redis_const, redis_client
from biz.models import User


class APILoginTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(mobile="16600000066", password="password")
        cls.client = cls.client_class()
        cls.authorization_header = dict(
            HTTP_AUTHORIZATION='Token {token}'.format(
                token=cls.client.post(
                    path="/login", data={"username": cls.user.mobile, "password": "password"}
                ).data['token']
            )
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        redis_client.redis_client.delete(redis_const.HAS_LOGINED.format(mobile="16600000066"))
