# -*- coding:utf-8 -*-
from biz.models import User
from rest_framework.test import APITestCase
from biz.models import Player


class AbilityTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(mobile='11111111111', password='password')

    def test_has_merits(self):
        res = self.client.get('/players/{}/ability'.format(self.user.id))
        self.assertEqual(res.status_code, 404)
        self.player = Player.objects.create(user_id=self.user.id, name='膜法师', mobile='11111111111',
                                            avatar='/path/to/face.jpg', stamina=50, skill=50, attack=50,
                                            defence=50, strength=60, willpower=70)
        res = self.client.get('/players/{}/ability'.format(self.user.id))
        self.assertEqual(res.status_code, 200)
