# -*- coding:utf-8 -*-
from rest_framework.test import APITestCase


class AbilityTest(APITestCase):
    def test_ability(self):
        res = self.client.get('/ability?skill=50&strength=80&defence=90&willpower=76&attack=86&stamina=83')
        self.assertEqual(res.status_code, 200)
        res = self.client.get('/ability')
        self.assertEqual(res.status_code, 400)
        res = self.client.get('/ability?skill=520&strength=820&defence=-1&willpower=76&attack=86&stamina=83')
        self.assertEqual(res.status_code, 400)
        res = self.client.get('/ability?skill=aa&strength=80&defence=90&willpower=76&attack=86&stamina=83')
        self.assertEqual(res.status_code, 400)
        res = self.client.get('/ability?skill=50&strength=80&defence=90')
        self.assertEqual(res.status_code, 400)
