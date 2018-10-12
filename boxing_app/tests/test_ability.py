# -*- coding:utf-8 -*-
from rest_framework.test import APITestCase
from biz.models import Player, User, Schedule, Match
from biz.constants import MATCH_CATEGORY_FREE_BOXING, SCHEDULE_STATUS_PUBLISHED, MATCH_CATEGORY_CHOICES, \
    MATCH_RESULT_RED_SUCCESS, MATCH_RESULT_BLUE_SUCCESS, MATCH_RESULT_RED_KO_BLUE, MATCH_RESULT_BLUE_KO_RED
from django.utils import timezone


class AbilityTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(mobile='11111111111', password='password')

    def test_ability_chart(self):
        res = self.client.get('/players/{}/ability_chart'.format(self.user.id))
        self.assertEqual(res.status_code, 404)
        self.player = Player.objects.create(user_id=self.user.id, name='膜法师', mobile='11111111111',
                                            avatar='/path/to/face.jpg', stamina=50, skill=50, attack=50,
                                            defence=50, strength=60, willpower=70)
        res = self.client.get('/players/{}/ability_chart'.format(self.user.id))
        self.assertEqual(res.status_code, 200)

    def test_ability_detail(self):
        res = self.client.get('/players/{}/ability_detail'.format(self.user.id))
        self.assertEqual(res.status_code, 404)
        self.player = Player.objects.create(user_id=self.user.id, name='膜法师', mobile='11111111111',
                                            avatar='/path/to/face.jpg', stamina=50, skill=50, attack=50,
                                            defence=50, strength=60, willpower=70)
        res = self.client.get('/players/{}/ability_detail'.format(self.user.id))
        self.assertEqual(res.status_code, 200)

    def test_player_match(self):
        res = self.client.get('/players/{}/match'.format(self.user.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['total'], 0)
        self.assertEqual(res.data['win'], 0)
        self.assertEqual(res.data['ko'], 0)
        self.assertEqual(len(res.data['results']), 0)

        race_date = timezone.now()
        avatar = '/path/to/face.jpg'
        level_min = 50
        level_max = 60
        ko_dict = {MATCH_RESULT_RED_KO_BLUE: 'red', MATCH_RESULT_BLUE_KO_RED: 'blue',
                   MATCH_RESULT_RED_SUCCESS: '',  MATCH_RESULT_BLUE_SUCCESS: ''}
        win_dict = {MATCH_RESULT_RED_SUCCESS: 'red', MATCH_RESULT_RED_KO_BLUE: 'red',
                    MATCH_RESULT_BLUE_SUCCESS: 'blue', MATCH_RESULT_BLUE_KO_RED: 'blue'}
        him = User.objects.create_user(mobile='22222222222', password='password')

        ta = Player.objects.create(user=self.user, name='长者', mobile='11111111111', avatar=avatar,
                                   stamina=88, skill=90, attack=90, defence=90, strength=90, willpower=79)
        he = Player.objects.create(user=him, name='香港记者', mobile='22222222222', avatar=avatar,
                                   stamina=88, skill=90, attack=90, defence=90, strength=90, willpower=79)

        s = Schedule.objects.create(name='大新闻', status=SCHEDULE_STATUS_PUBLISHED, race_date=race_date)
        m = Match.objects.create(red_player=ta, blue_player=he, schedule=s, category=MATCH_CATEGORY_FREE_BOXING,
                                 level_min=level_min, level_max=level_max, result=MATCH_RESULT_RED_KO_BLUE)

        res = self.client.get('/players/{}/match'.format(self.user.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['total'], 1)
        self.assertEqual(res.data['win'], 1)
        self.assertEqual(res.data['ko'], 1)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['red_player'], self.user.id)
        self.assertEqual(res.data['results'][0]['red_avatar'], avatar)
        self.assertEqual(res.data['results'][0]['red_name'], ta.name)
        self.assertEqual(res.data['results'][0]['blue_name'], he.name)
        self.assertEqual(res.data['results'][0]['blue_avatar'], avatar)
        self.assertEqual(res.data['results'][0]['blue_player'], him.id)
        self.assertEqual(res.data['results'][0]['schedule'], s.name)
        self.assertEqual(res.data['results'][0]['category'], dict(MATCH_CATEGORY_CHOICES)[MATCH_CATEGORY_FREE_BOXING])
        self.assertEqual(res.data['results'][0]['level_min'], level_min)
        self.assertEqual(res.data['results'][0]['level_max'], level_max)
        self.assertEqual(res.data['results'][0]['time'], race_date.date())
        self.assertEqual(res.data['results'][0]['ko'], ko_dict[m.result])
        self.assertEqual(res.data['results'][0]['win'], win_dict[m.result])
