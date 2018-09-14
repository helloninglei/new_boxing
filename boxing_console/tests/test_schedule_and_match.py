from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import Schedule, User, Player, Match
from datetime import datetime
from biz.constants import SCHEDULE_STATUS_PUBLISHED, MATCH_CATEGORY_BOXING, MATCH_RESULT_BLUE_SUCCESS


class ScheduleMatchTestCase(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user = User.objects.create_superuser(mobile="19080090990", password="password")
        self.user2 = User.objects.create_superuser(mobile="19088989763", password="password")
        self.client.login(username=self.user.mobile, password="password")

    def test_should_create_schedule(self):
        data = {"name": "终极格斗冠军赛", "race_date": "2018-09-21"}
        response = self.client.post(path="/schedules", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        schedule = Schedule.objects.filter(operator=self.user).first()
        self.assertEqual(schedule.name, data['name'])
        self.assertEqual(schedule.race_date, datetime.strptime(data['race_date'], "%Y-%m-%d").date())

    def test_should_get_order_schedule_list(self):
        schedule1 = Schedule.objects.create(name="终极格斗冠军赛", race_date="2018-09-21")
        schedule2 = Schedule.objects.create(name="世界职业拳击比赛", race_date="2018-10-21", status=SCHEDULE_STATUS_PUBLISHED)
        response = self.client.get(path="/schedules")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        result = response.data['results']
        self.assertEqual(result[0]['id'], schedule2.id)
        self.assertEqual(result[0]['name'], schedule2.name)
        self.assertEqual(result[0]['status'], "已发布")
        self.assertEqual(result[1]['id'], schedule1.id)
        self.assertEqual(result[1]['name'], schedule1.name)
        self.assertEqual(result[1]['status'], "未发布")

    def test_should_update_schedule_list(self):
        schedule = Schedule.objects.create(name="终极格斗冠军赛", race_date="2018-09-21")
        data = {"name": "世界职业拳击比赛", "race_date": "2018-10-21"}
        response = self.client.put(path=f"/schedules/{schedule.id}", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schedule.refresh_from_db()
        self.assertEqual(schedule.name, data['name'])
        self.assertEqual(schedule.race_date, datetime.strptime(data['race_date'], "%Y-%m-%d").date())
        data = {"name": "终极格斗冠军赛", "race_date": "2018-09-21"}
        response = self.client.patch(path=f"/schedules/{schedule.id}", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schedule.refresh_from_db()
        self.assertEqual(schedule.name, data['name'])
        self.assertEqual(schedule.race_date, datetime.strptime(data['race_date'], "%Y-%m-%d").date())

    def test_should_get_player_list(self):
        player = Player.objects.create(**self.player_data, mobile=self.user.mobile)
        response = self.client.get(path="/players")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], player.name)
        self.assertEqual(response.data['results'][0]['mobile'], player.mobile)

    def test_should_create_match(self):
        player1 = Player.objects.create(**self.player_data, mobile=self.user2.mobile)
        player2 = Player.objects.create(mobile=self.user.mobile, **self.player_data)
        schedule = Schedule.objects.create(name="终极格斗冠军赛", race_date="2018-09-21")
        data = dict(blue_player=player1.id, red_player=player2.id, schedule=schedule.id, category=MATCH_CATEGORY_BOXING,
                    level_min=20, level_max=100, result=MATCH_RESULT_BLUE_SUCCESS)
        response = self.client.post(path="/matches", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Match.objects.filter(blue_player=player1).exists())

    def test_should_not_create_match(self):
        schedule = Schedule.objects.create(name="终极格斗冠军赛", race_date="2018-09-21")
        data = dict(blue_player=6, red_player=6, schedule=schedule.id, category=6,
                    level_min=20, level_max=100, result=6)
        response = self.client.post(path="/matches", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['category'][0], "对战类型不符合要求!")
        self.assertEqual(response.data['result'][0], "对战结果不符合要求!")
        self.assertEqual(response.data['blue_player'][0], '无效主键 “6” － 对象不存在。')
        self.assertEqual(response.data['red_player'][0], '无效主键 “6” － 对象不存在。')
        player1 = Player.objects.create(**self.player_data, mobile=self.user2.mobile)
        data.update(blue_player=player1.id, red_player=player1.id, category=MATCH_CATEGORY_BOXING,
                    result=MATCH_RESULT_BLUE_SUCCESS)
        response = self.client.post(path="/matches", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "红方和蓝方不能是同一拳手!")
        player2 = Player.objects.create(mobile=self.user.mobile, **self.player_data)
        data.update(red_player=player2.id, level_min=100, level_max=20)
        response = self.client.post(path="/matches", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "项目级别不符合要求!")

    @property
    def player_data(self):
        return {
            "name": "name", "avatar": "avatar1.png", "stamina": 10, "skill": 10, "attack": 10, "defence": 10,
            "strength": 10, "willpower": 10, "user": self.user
        }
