from rest_framework.test import APITestCase

from biz.models import User


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

    def test_get_club_list(self):
        res = self.client1.get('/clubs')
        print(res)