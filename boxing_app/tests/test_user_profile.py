from rest_framework import status

from biz.constants import DEFAULT_BIO_OF_MEN, DEFAULT_BIO_OF_WOMEN, USER_TYPE_CELEBRITY, DEFAULT_NICKNAME_FORMAT, \
    DEFAULT_AVATAR
from biz.models import UserProfile, User
from biz.services.url_service import get_cdn_url
from . import APILoginTestCase


class UserProfileTestCase(APILoginTestCase):
    def setUp(self):
        self.user_profile_data = dict(user=self.user, name="姓名", gender=False, nick_name="昵称", nation="汉族", weight=70,
                                      height=180, profession="职业", avatar="头像", bio="个性签名")
        UserProfile.objects.filter(user=self.user).update(**self.user_profile_data)
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
        self.assertEqual(response.data['avatar'], get_cdn_url(self.user_profile_data['avatar']))
        self.assertEqual(response.data['bio'], self.user_profile_data['bio'])

        user = User.objects.create_user(mobile="19900000002", password="p")
        response = self.client.get(path=f"/user_profile/{user.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nick_name'], DEFAULT_NICKNAME_FORMAT.format(user.id))
        self.assertEqual(response.data['avatar'], DEFAULT_AVATAR)

    def test_user_profile_bio_is_none(self):
        user = User.objects.create_user(mobile="18877778888", password="password", user_type=USER_TYPE_CELEBRITY,
                                        title="我是大名人")
        response = self.client.get(path=f"/user_profile/{user.id}")
        self.assertEqual(response.data['bio'], DEFAULT_BIO_OF_MEN)
        self.assertEqual(response.data['user_type'], user.get_user_type_display())
        self.assertEqual(response.data['title'], user.title)
        UserProfile.objects.filter(user=user).update(gender=False)
        response = self.client.get(path=f"/user_profile/{user.id}")
        self.assertEqual(response.data['bio'], DEFAULT_BIO_OF_WOMEN)

    def test_change_avatar(self):
        data = {"avatar": "新头像"}
        response = self.client.put(path="/user_profile_patch", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.get(id=self.user.user_profile.id).avatar, data['avatar'])

    def test_change_nick_name(self):
        data = {"nick_name": "新昵称"}
        response = self.client.put(path="/user_profile_patch", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_profile = UserProfile.objects.get(pk=self.user.user_profile.id)
        self.assertEqual(user_profile.nick_name, data['nick_name'])
        self.assertEqual(user_profile.nick_name_index_letter, 'X')

        data = {"nick_name": "1新昵称"}
        response = self.client.put(path="/user_profile_patch", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_profile = UserProfile.objects.get(pk=self.user.user_profile.id)
        self.assertEqual(user_profile.nick_name, data['nick_name'])
        self.assertEqual(user_profile.nick_name_index_letter, '#')

    def test_gender_should_change(self):
        data = {"gender": not self.user_profile_data['gender']}
        response = self.client.put(path="/user_profile_patch", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIs(UserProfile.objects.get(user=self.user).gender, data['gender'])

    def test_update_user_profile(self):
        self.assertFalse(UserProfile.objects.get(user=self.user).gender)
        data = {
            "birthday": "2018-05-17", "height": "190", "name": "改名字", "nation": "民族", "profession": "医生",
            "weight": "90"
        }
        response = self.client.put(path="/user_profile", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.get(id=self.user.user_profile.id).name, data['name'])
        self.assertEqual(UserProfile.objects.get(id=self.user.user_profile.id).profession, data['profession'])
        self.assertFalse(UserProfile.objects.get(user=self.user).gender)

        data.pop("weight")
        response = self.client.put(path="/user_profile", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['weight'][0], "该字段是必填项。")

    def test_batch_user_profile(self):
        user1 = User.objects.create_user(mobile="13434345434", password="password")
        user2 = User.objects.create_user(mobile="13434345435", password="password")
        client = self.client_class()
        response = client.get(path="/batch_user_profile", data={"user_ids": f"{user2.id},{user1.id}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
