from datetime import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, Player, Match, Schedule


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

    def test_player_list(self):
        self.player_data.update(name="张三", user=self.user1)
        Player.objects.create(**self.player_data)
        self.player_data.update(name="李四", mobile=self.user2.mobile, user=self.user2)
        Player.objects.create(**self.player_data)
        res = self.client.get('/player')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

        # search by name
        res = self.client.get('/player', data={"search": "张三"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        res = self.client.get('/player', data={"search": "张四"})
        self.assertEqual(len(res.data['results']), 0)

        # search by mobile
        res = self.client.get('/player', data={"search": self.user1.mobile})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        res = self.client.get('/player', data={"search": 11111111113})
        self.assertEqual(len(res.data['results']), 0)

    def test_get_player_detail(self):
        self.player_data.update(user=self.user1)
        player = Player.objects.create(**self.player_data)
        res = self.client.get(f'/player/{player.pk}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for key in self.player_data:
            if key != 'user':
                self.assertEqual(res.data[key], self.player_data[key])

    def test_delete_player(self):
        # delete success
        self.player_data.update(user=self.user1)
        self.assertEqual(Player.objects.all().count(), 0)
        player = Player.objects.create(**self.player_data)
        self.assertEqual(Player.objects.all().count(), 1)
        res = self.client.delete(f'/player/{player.pk}')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Player.objects.all().count(), 0)

        # delete fail because player has match
        player1 = Player.objects.create(**self.player_data)
        self.player_data.update(mobile=self.user2.mobile, user=self.user2)
        player2 = Player.objects.create(**self.player_data)
        self.assertEqual(Player.objects.all().count(), 2)
        schedule = Schedule.objects.create(**{
            "name": "schedule01",
            "race_date": datetime.today()
        })
        Match.objects.create(**{
            "red_player": player1,
            "blue_player": player2,
            "schedule": schedule,
            "category": constants.MATCH_CATEGORY_MMA,
            "level_min": 100,
            "level_max": 120,
            "result": constants.MATCH_RESULT_RED_SUCCESS
        })
        res = self.client.delete(f'/player/{player1.pk}')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "请先删除该参赛拳手的所有赛程再删除拳手记录")
        self.assertEqual(Player.objects.all().count(), 2)

        # delete success if delete math
        Match.objects.all().delete()
        res = self.client.delete(f'/player/{player1.pk}')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Player.objects.all().count(), 1)

    def test_update_player(self):
        self.player_data.update(user=self.user1)
        player1 = Player.objects.create(**self.player_data)
        self.player_data.update(user=self.user2, mobile=self.user2.mobile)
        player2 = Player.objects.create(**self.player_data)
        update_data = {
            "name": "赵六",
            "mobile": self.user2.mobile,
            "avatar": "avatar2.png",
            "stamina": 1,
            "skill": 1,
            "attack": 1,
            "defence": 1,
            "strength": 1,
            "willpower": 1
        }
        # mobile is another player
        res = self.client.post(f'/player/{player1.id}', data=update_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # mobile is not user
        update_data.update(mobile="11011011000")
        res = self.client.post(f'/player/{player1.id}', data=update_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # mobile is validate
        update_data.update(mobile=self.user1.mobile)
        res = self.client.post(f'/player/{player1.id}', data=update_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for key in update_data:
            self.assertEqual(res.data[key], update_data[key])
