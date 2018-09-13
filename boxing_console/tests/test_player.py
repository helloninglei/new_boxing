from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from biz.models import User, Player


class PlayerTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(mobile='11111111111', password='password')
        self.user2 = User.objects.create_superuser(mobile='11111111112', password='password')
        self.client = self.client_class()
        self.client.login(username=self.user1, password='password')
        self.player_data = {
            "name": "user1",
            "mobile": self.user1.mobile,
            "avatar": "avatar1.png",
            "stamina": 10,
            "skill": 10,
            "attack": 10,
            "defence": 10,
            "strength": 10,
            "willpower": 10
        }

    def test_create_player_fail(self):
        # failed becaust player not a user
        self.player_data.update(mobile='11111111113')
        res = self.client.post(reverse('create_player'), data=self.player_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # failed because player is created before
        self.player_data.update(mobile=self.user1.mobile, user=self.user1)
        Player.objects.create(**self.player_data)
        res = self.client.post(reverse('create_player'), data=self.player_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_player_success(self):
        res = self.client.post(reverse('create_player'), data=self.player_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in self.player_data:
            self.assertEqual(res.data[key], self.player_data[key])