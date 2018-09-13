from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from biz.models import User, Player, UserProfile


class CheckPlayerMobileTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(mobile='11111111111', password='password')
        self.user2 = User.objects.create_superuser(mobile='11111111112', password='password')
        self.user3 = User.objects.create_superuser(mobile='11111111113', password='password')
        self.player = Player.objects.create(**{
            "name": "user1",
            "mobile": self.user2.mobile,
            "avatar": "avatar1.png",
            "stamina": 10,
            "skill": 10,
            "attack": 10,
            "defence": 10,
            "strength": 10,
            "willpower": 10,
            "user": self.user2,
        })
        self.client = self.client_class()
        self.client.login(username=self.user3, password='password')

    def test_check_player_mobile(self):
        mobile0 = "11111111110"
        mobile1 = self.user1.mobile
        mobile2 = self.user2.mobile
        UserProfile.objects.filter(user__in=(self.user1, self.user2)).update(avatar="avatar.png")

        # mobile0 is not user
        res = self.client.get(reverse('check_player_mobile'), data={"mobile": mobile0})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(res.data['is_user'])
        self.assertFalse(res.data['is_player'])
        self.assertIsNone(res.data['avatar'])

        # mobile1 is user but not player
        res = self.client.get(reverse('check_player_mobile'), data={"mobile": mobile1})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['is_user'])
        self.assertFalse(res.data['is_player'])
        self.assertIsNotNone(res.data['avatar'])

        # mobile2 is user and is player
        res = self.client.get(reverse('check_player_mobile'), data={"mobile": mobile2})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['is_user'])
        self.assertTrue(res.data['is_player'])
        self.assertIsNotNone(res.data['avatar'])

