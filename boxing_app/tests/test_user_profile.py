from rest_framework import status
from biz.models import UserProfile
from . import APILoginTestCase


class UserProfileTestCase(APILoginTestCase):
    def setUp(self):
        UserProfile.objects.create(user=self.user, name="姓名", gender=False, nick_name="昵称", nation="汉族", weight=70,
                                   height=180, profession="职业", avatar="头像", bio="个性签名")
        self.client.credentials(**self.authorization_header)

    def test_user_profile_detail(self):
        response = self.client.get(path="/user_profile")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "姓名")
        self.assertEqual(response.data['gender'], False)
        self.assertEqual(response.data['nick_name'], "昵称")
        self.assertEqual(response.data['nation'], "汉族")
        self.assertEqual(response.data['height'], '180')
        self.assertEqual(response.data['weight'], '70')
        self.assertEqual(response.data['profession'], "职业")
        self.assertEqual(response.data['avatar'], "头像")
        self.assertEqual(response.data['bio'], "个性签名")

    def test_change_avatar(self):
        response = self.client.patch(path="/user_profile", data={"avatar": "新头像"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.get(id=self.user.user_profile.id).avatar, "新头像")

    def test_change_nick_name(self):
        response = self.client.patch(path="/user_profile", data={"nick_name": "新昵称"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.get(id=self.user.user_profile.id).nick_name, "新昵称")

    def test_update_user_profile(self):
        response = self.client.put(path="/user_profile", data={
            "birthday": "2018-05-17 17:12:18", "height": "190", "name": "改名字", "nation": "民族", "profession": "医生",
            "weight": "90"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.get(id=self.user.user_profile.id).name, "改名字")
        self.assertEqual(UserProfile.objects.get(id=self.user.user_profile.id).profession, "医生")

        response = self.client.put(path="/user_profile", data={
            "birthday": "2018-05-17 17:12:18", "height": "190", "name": "改名字", "nation": "民族", "profession": "医生",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['weight'][0], "该字段是必填项。")
