from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import Schedule, User
from datetime import datetime


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
