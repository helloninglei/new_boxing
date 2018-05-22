from rest_framework import status
from biz.models import UserProfile
from . import APILoginTestCase


class UserProfileTestCase(APILoginTestCase):
    def setUp(self):
        self.user_profile_data = dict(user=self.user, name="姓名", gender=False, nick_name="昵称", nation="汉族", weight='70',
                                      height='180', profession="职业", avatar="头像", bio="个性签名")
        UserProfile.objects.create(**self.user_profile_data)
        self.client.credentials(**self.authorization_header)

    def test_user_profile_detail(self):
        response = self.client.get(path="/user_profile")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.user_profile_data['name'])
        self.assertEqual(response.data['gender'], self.user_profile_data['gender'])
        self.assertEqual(response.data['nick_name'], self.user_profile_data['nick_name'])
        self.assertEqual(response.data['nation'], self.user_profile_data['nation'])
        self.assertEqual(response.data['height'], self.user_profile_data['height'])
        self.assertEqual(response.data['weight'], self.user_profile_data['weight'])
        self.assertEqual(response.data['profession'], self.user_profile_data['profession'])
        self.assertEqual(response.data['avatar'], self.user_profile_data['avatar'])
        self.assertEqual(response.data['bio'], self.user_profile_data['bio'])

    def test_change_avatar(self):
        data = {"avatar": "新头像"}
        response = self.client.patch(path="/user_profile", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.get(id=self.user.user_profile.id).avatar, data['avatar'])

    def test_change_nick_name(self):
        data = {"nick_name": "新昵称"}
        response = self.client.patch(path="/user_profile", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.get(id=self.user.user_profile.id).nick_name, data['nick_name'])

    def test_update_user_profile(self):
        data = {
            "birthday": "2018-05-17", "height": "190", "name": "改名字", "nation": "民族", "profession": "医生",
            "weight": "90"
        }
        response = self.client.put(path="/user_profile", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.get(id=self.user.user_profile.id).name, data['name'])
        self.assertEqual(UserProfile.objects.get(id=self.user.user_profile.id).profession, data['profession'])

        data.pop("weight")
        response = self.client.put(path="/user_profile", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['weight'][0], "该字段是必填项。")