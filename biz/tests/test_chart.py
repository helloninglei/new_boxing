# -*- coding:utf-8 -*-

import unittest
import io
from biz.services.chart_service import make_radar


class ChartTestCase(unittest.TestCase):
    def test_chart(self):
        res = make_radar(0)
        self.assertIsNone(res)
        res = make_radar('hello')
        self.assertIsNone(res)
        res = make_radar(True)
        self.assertIsNone(res)
        res = make_radar([1, 2, 3])
        self.assertIsNone(res)
        res = make_radar([1, 2, 3, 4, 5, 6, ])
        self.assertTrue(isinstance(res, type(io.BytesIO())))
        self.assertNotEqual(len(res.read()), 0)
