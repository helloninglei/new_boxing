from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import Schedule, User
from datetime import datetime
from biz.constants import SCHEDULE_STATUS_PUBLISHED


class ScheduleTestCase(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user = User.objects.create_superuser(mobile="19080090990", password="password")
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
