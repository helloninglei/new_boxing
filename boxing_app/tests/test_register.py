from rest_framework import status
from rest_framework.test import APITestCase
from biz.models import User, UserProfile
from biz import redis_const, redis_client
from biz.constants import SERVICE_USER_ID


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        User.objects.create_user(mobile="19900000000", password="password")

    def test_mobile_register_status(self):
        response = self.client.get(path="/mobile_register_status", data={"mobile": "19900000000"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['result'])

        response = self.client.get(path="/mobile_register_status", data={"mobile": "19900000001"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['result'])

    def test_register(self):
        mobile = "18800000000"
        redis_client.redis_client.setex(redis_const.SEND_VERIFY_CODE.format(mobile=mobile), 300, "123456")

        response = self.client.post(path="/register",
                                    data={"mobile": mobile, "password": "password", "verify_code": "123456"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(redis_client.redis_client.exists(redis_const.REGISTER_INFO.format(mobile=mobile)))
        self.assertEqual(response.data['result'], "ok")
        response = self.client.post(path="/register_with_user_info", data={
            "mobile": mobile, "gender": True, "avatar": "avatar", "nick_name": "nick_name"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['result'], "ok")
        self.assertTrue(User.objects.filter(mobile=mobile))
        self.assertTrue(UserProfile.objects.filter(user__mobile=mobile).exists())
        self.assertFalse(redis_client.redis_client.exists(redis_const.REGISTER_INFO.format(mobile=mobile)))
        user = User.objects.get(mobile=mobile)
        self.assertTrue(redis_client.is_following(user.id, SERVICE_USER_ID))

    def test_social_register(self):
        mobile = "18800000011"
        redis_client.redis_client.setex(redis_const.SEND_VERIFY_CODE.format(mobile=mobile), 300, "123456")
        response = self.client.post(path="/register",
                                    data={"mobile": mobile, "password": "password", "verify_code": "123456",
                                          "wechat_openid": "111", "weibo_openid": "222"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "不能同时给微信和微博绑定手机号!")
        user = User.objects.create_user(mobile=mobile, password="password")
        response = self.client.post(path="/register",
                                    data={"mobile": mobile, "password": "password", "verify_code": "123456"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'][0], "手机号已存在！")

        user.delete()

        response = self.client.post(path="/register",
                                    data={"mobile": mobile, "password": "password", "verify_code": "123456",
                                          "wechat_openid": "111"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(redis_client.redis_client.exists(redis_const.REGISTER_INFO.format(mobile=mobile)))
        self.assertEqual(response.data['result'], "ok")

        response = self.client.post(path="/register_with_user_info", data={
            "mobile": mobile, "gender": True, "avatar": "avatar", "nick_name": "nick_name"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['result'], "ok")
        self.assertTrue(User.objects.filter(mobile=mobile))
        self.assertEqual(User.objects.get(mobile=mobile).wechat_openid, "111")
        self.assertFalse(redis_client.redis_client.exists(redis_const.REGISTER_INFO.format(mobile=mobile)))
        user = User.objects.get(mobile=mobile)
        self.assertTrue(redis_client.is_following(user.id, SERVICE_USER_ID))
        self.assertEqual(UserProfile.objects.get(user=user).nick_name_index_letter, "N")

        user.delete()

        response = self.client.post(path="/register",
                                    data={"mobile": mobile, "password": "password", "verify_code": "123456",
                                          "wechat_openid": "111"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(redis_client.redis_client.exists(redis_const.REGISTER_INFO.format(mobile=mobile)))
        self.assertEqual(response.data['result'], "ok")

        response = self.client.post(path="/register_with_user_info", data={
            "mobile": mobile, "gender": True, "avatar": "avatar", "nick_name": "1223"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['result'], "ok")
        self.assertTrue(User.objects.filter(mobile=mobile))
        self.assertEqual(User.objects.get(mobile=mobile).wechat_openid, "111")
        self.assertFalse(redis_client.redis_client.exists(redis_const.REGISTER_INFO.format(mobile=mobile)))
        user = User.objects.get(mobile=mobile)
        self.assertTrue(redis_client.is_following(user.id, SERVICE_USER_ID))
        self.assertEqual(UserProfile.objects.get(user=user).nick_name_index_letter, "#")

        user.delete()

        user = User.objects.create_user(mobile="00000111111", password="password", weibo_openid="1111")
        response = self.client.post(path="/register",
                                    data={"mobile": mobile, "password": "password", "verify_code": "123456",
                                          "weibo_openid": "1111"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(redis_client.redis_client.exists(redis_const.REGISTER_INFO.format(mobile=mobile)))
        self.assertEqual(response.data['result'], "ok")
        response = self.client.post(path="/register_with_user_info", data={
            "mobile": mobile, "gender": True, "avatar": "avatar", "nick_name": "nick_name"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['result'], "ok")
        self.assertEqual(user.id, User.objects.get(mobile=mobile).id)
        self.assertEqual(User.objects.get(pk=user.id).mobile, mobile)
