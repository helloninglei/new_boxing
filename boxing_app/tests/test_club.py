from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from biz.models import User, BoxingClub


class ClubTestCase(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(mobile='11111111111', password='password')
        self.client1 = self.client_class()
        self.client1.login(username=self.test_user_1, password='password')
        self.club_data = {
            "name": "拳王01",
            "address": "丰台区角门东洋桥",
            "longitude": 111.123456,
            "latitude": 11.123456,
            "phone": "11111111111",
            "city": "北京市",
            "opening_hours": "10:00--20:00",
            "images": ["www.baidu.com", "www.sina.com.cn"],
            "introduction": "最牛逼的拳馆"
        }

    def test_club_list_and_detail(self):
        club = BoxingClub.objects.create(**self.club_data)

        # 获取拳馆列表
        res = self.client1.get('/clubs')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)

        # 通过城市名筛选拳馆列表
        res = self.client1.get('/clubs', data={'city': self.club_data["city"]})
        self.assertEqual(len(res.data['results']), 1)
        res = self.client1.get('/clubs', data={'city': 'unknown_city'})
        self.assertEqual(len(res.data['results']), 0)

        # 获取拳馆详情
        res = self.client1.get(reverse('club-detail', kwargs={'pk': club.pk}))
        for key in self.club_data:
            self.assertEqual(self.club_data[key], res.data[key])
