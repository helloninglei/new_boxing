import json

from django.test import TestCase
from rest_framework import status

from biz import redis_client
from biz.models import User, BoxingClub


class BoxingClubTestCase(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_superuser(mobile='11111111111', password='password')
        self.client = self.client_class()
        self.client.login(username=self.test_user1, password='password')
        self.data = {
                    "name": "拳王01",
                    "address": "丰台区角门东洋桥",
                    "longitude": 111.123456,
                    "latitude": 11.123456,
                    "phone": "11111111111",
                    "opening_hours": "10:00--20:00",
                    "images": ["www.baidu.com", "www.sina.com.cn"],
                    "introduction": "最牛逼的拳馆"
                    }

    def test_create_club(self):
        res = self.client.post('/club', self.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # 判断拳馆已正确创建
        for key in self.data.keys():
            if key in ("longitude", "latitude"):
                self.assertEqual(res.data[key], str(self.data.get(key)))
            else:
                self.assertEqual(res.data[key], self.data.get(key))
        # 判断redis中已记录位置信息
        redis_location_record = redis_client.get_boxing_club_location(res.data['id'])
        self.assertAlmostEqual(self.data['longitude'], redis_location_record[0][0], delta=0.00001)
        self.assertAlmostEqual(self.data['latitude'], redis_location_record[0][1], delta=0.00001)

    def test_get_club_detail(self):
        create_res = self.client.post('/club', self.data)
        detail_res = self.client.get(f'/club/{create_res.data["id"]}')
        for key in self.data.keys():
            if key in ("longitude", "latitude"):
                self.assertEqual(detail_res.data[key], str(self.data.get(key)))
            else:
                self.assertEqual(detail_res.data[key], self.data.get(key))

    def test_create_fail_with_repetition_club_name(self):
        self.client.post('/club', self.data)
        res = self.client.post('/club', self.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_club(self):
        create_res = self.client.post('/club', self.data)
        self.data['longitude'] = 122.123456
        self.data['latitude'] = 22.123456
        update_res = self.client.put(f'/club/{create_res.data["id"]}',
                                     json.dumps(self.data), content_type='application/json')
        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        # 判断拳馆数据已更新
        for key in self.data.keys():
            if key in ("longitude", "latitude"):
                self.assertEqual(update_res.data[key], str(self.data.get(key)))
            else:
                self.assertEqual(update_res.data[key], self.data.get(key))
        redis_location_record = redis_client.get_boxing_club_location(update_res.data['id'])
        # 判断redis中位置记录已更新
        self.assertAlmostEqual(self.data['longitude'], redis_location_record[0][0], delta=0.00001)
        self.assertAlmostEqual(self.data['latitude'], redis_location_record[0][1], delta=0.00001)

    def test_delete_club(self):
        create_res = self.client.post('/club', self.data)
        delete_res = self.client.delete(f'/club/{create_res.data["id"]}')
        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        # 判断拳馆已删除
        self.assertFalse(BoxingClub.objects.filter(id=create_res.data['id']).exists())
        # 判断redis记录已删除
        redis_location_record = redis_client.get_boxing_club_location(create_res.data['id'])
        self.assertIsNone(redis_location_record[0])

    def test_club_list(self):
        data1 = {
            "name": "拳王01",
            "address": "丰台区",
            "longitude": 111.111111,
            "latitude": 11.111111,
            "phone": "11111111111",
            "opening_hours": "10:00--20:00",
            "images": ["www.baidu01.com", "www.sina01.com.cn"],
            "introduction": "最牛逼的拳馆"
        }
        data2 = {
            "name": "拳王02",
            "address": "朝阳区",
            "longitude": 112.111111,
            "latitude": 12.111111,
            "phone": "11111111112",
            "opening_hours": "10:00--20:00",
            "images": ["www.baidu02.com", "www.sina02.com.cn"],
            "introduction": "最善良的拳馆"
        }
        data3 = {
            "name": "拳王03",
            "address": "海淀区",
            "longitude": 113.111111,
            "latitude": 13.111111,
            "phone": "11111111113",
            "opening_hours": "10:00--20:00",
            "images": ["www.baidu03.com", "www.sina03.com.cn"],
            "introduction": "最火爆的拳馆"
        }
        BoxingClub.objects.bulk_create([BoxingClub(**data) for data in (data1, data2, data3)])

        # 获取拳馆列表，并验证数据
        list_res = self.client.get('/club')
        self.assertEqual(list_res.status_code, status.HTTP_200_OK)
        self.assertEqual(list_res.data['count'], 3)
        for key in data1:
            if key in ("longitude", "latitude"):
                self.assertEqual(str(data1[key]), list_res.data['results'][0].get(key))
            else:
                self.assertEqual(data1[key], list_res.data['results'][0].get(key))

        # 通过拳馆名进行搜索,并验证结果
        search_res = self.client.get('/club', data={'search': data2['name']})
        self.assertEqual(search_res.data['count'], 1)
        for key in data2:
            if key in ("longitude", "latitude"):
                self.assertEqual(str(data2[key]), search_res.data['results'][0].get(key))
            else:
                self.assertEqual(data2[key], search_res.data['results'][0].get(key))
