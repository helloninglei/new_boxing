import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from biz import constants
from biz.models import User, BoxerIdentification, Player, UserProfile


class SyncDataTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(mobile='11111111111', password='password')
        self.client = self.client_class()
        self.client.login(username=self.test_user, password='password')
        self.user_profile_data = dict(user=self.test_user, name="张三", gender=False, nick_name="昵称", nation="汉族", weight=70,
                                      height=180, profession="职业", avatar="头像", bio="个性签名", birthday="2018-05-17")
        self.boxer_data = {
            "user": self.test_user,
            "real_name": "张三",
            "height": 190,
            "weight": 120,
            "birthday": "2018-04-25",
            "identity_number": "131313141444141444",
            "mobile": "113134",
            "is_professional_boxer": True,
            "club": "131ef2f3",
            "job": '老师',
            "introduction": "beautiful",
            "experience": '',
            "honor_certificate_images": ['http://img1.com', 'http://img2.com', 'http://img3.com'],
            "competition_video": '',
            "authentication_state": constants.BOXER_AUTHENTICATION_STATE_WAITING
        }
        self.player_data = {
            "user": self.test_user,
            "name": "张三",
            "mobile": self.test_user.mobile,
            "avatar": "avatar1.png",
            "stamina": 10,
            "skill": 10,
            "attack": 10,
            "defence": 10,
            "strength": 10,
            "willpower": 10
        }

    def test_check_user_realname(self):
        # success
        res = self.client.put('/user_profile', data=self.user_profile_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # fail because name is not hanz
        self.user_profile_data.update(name="zhangsan")
        res = self.client.put('/user_profile', data=self.user_profile_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # fail because name is more than 6 words
        self.user_profile_data.update(name="张三张三张三哈")
        res = self.client.put('/user_profile', data=self.user_profile_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_nation(self):
        # success
        res = self.client.put('/user_profile', data=self.user_profile_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # fail because nation is not hanz
        self.user_profile_data.update(nation="hanzu")
        res = self.client.put('/user_profile', data=self.user_profile_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # fail because nation is more than 5 words
        self.user_profile_data.update(nation="汉族汉族汉族")
        res = self.client.put('/user_profile', data=self.user_profile_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_profession(self):
        # success
        res = self.client.put('/user_profile', data=self.user_profile_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # fail because profession is more than 5 words
        self.user_profile_data.update(profession="老师老师老师老师老师哈")
        res = self.client.put('/user_profile', data=self.user_profile_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sync_user_profile(self):
        # test for sync user real name
        new_name = "赵六"
        BoxerIdentification.objects.create(**self.boxer_data)
        Player.objects.create(**self.player_data)
        user_profile = UserProfile.objects.get(user=self.test_user)
        boxer = BoxerIdentification.objects.get(user=self.test_user)
        player = Player.objects.get(user=self.test_user)
        user_profile.name = new_name
        user_profile.save()
        user_profile.refresh_from_db()
        boxer.refresh_from_db()
        player.refresh_from_db()
        self.assertEqual(user_profile.name, new_name)
        self.assertEqual(boxer.real_name, new_name)
        self.assertEqual(player.name, new_name)

        # test for sync user height
        new_height = 180
        boxer.height = new_height
        boxer.save()
        boxer.refresh_from_db()
        user_profile.refresh_from_db()
        self.assertEqual(boxer.height, new_height)
        self.assertEqual(user_profile.height, new_height)

        # test for sync user weight
        new_weight = 100
        user_profile.weight = new_weight
        user_profile.save()
        boxer.refresh_from_db()
        user_profile.refresh_from_db()
        self.assertEqual(boxer.weight, new_weight)
        self.assertEqual(user_profile.weight, new_weight)

        # test for sync birthday
        new_birthday = datetime.datetime.today().date()
        boxer.birthday = new_birthday
        boxer.save()
        boxer.refresh_from_db()
        user_profile.refresh_from_db()
        self.assertEqual(user_profile.birthday, new_birthday)
        self.assertEqual(boxer.birthday, new_birthday)

        # test for sync profession
        new_profession = "程序员"
        user_profile.profession = new_profession
        user_profile.save()
        user_profile.refresh_from_db()
        boxer.refresh_from_db()
        self.assertEqual(boxer.job, new_profession)
        self.assertEqual(user_profile.profession, new_profession)
