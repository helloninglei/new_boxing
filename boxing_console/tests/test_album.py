# -*- coding:utf-8 -*-
import json

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User
from biz.models import UserProfile, AlbumPicture


class AlbumTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_superuser(mobile='11111111111', password='password')
        self.nick_name = '膜法师'
        UserProfile.objects.filter(user=self.test_user).update(nick_name='膜法师')
        self.client = self.client_class()
        self.client.login(username=self.test_user, password='password')
        self.data_album = {"name": "他改变了中国", "release_time": "1926-08-17 20:12:01",
                           "is_show": False, "related_account": self.test_user.id}
        self.data_picture = [{"picture": "/uploads/52/a9/a96d7356a482ecc732c8b1f67b372717fb80.jpg"}]

    def test_create_album(self):
        res = self.client.post(reverse('album_list'), self.data_album)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], self.data_album['name'])
        self.assertEqual(res.data['release_time'], self.data_album['release_time'])
        self.assertFalse(res.data['is_show'])
        self.assertEqual(res.data['related_account'], self.test_user.id)
        self.assertEqual(res.data['nick_name'], self.nick_name)

    def test_get_album_list(self):
        album_count = 15
        for i in range(album_count):
            self.client.post(reverse('album_list'), self.data_album)
        res = self.client.get(reverse('album_list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], album_count)
        self.assertIsNotNone(res.data['next'])
        self.assertIsNone(res.data['previous'])
        self.assertEqual(len(res.data['results']), 10)

    def test_get_album_info(self):
        response = self.client.post(reverse('album_list'), self.data_album)
        album_id = response.data['id']
        res = self.client.get(reverse('album_modify', kwargs={'pk': album_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], self.data_album['name'])
        self.assertEqual(res.data['release_time'], self.data_album['release_time'])
        self.assertEqual(res.data['is_show'], self.data_album['is_show'])
        self.assertEqual(res.data['related_account'], self.test_user.id)
        self.assertEqual(res.data['nick_name'], self.nick_name)

    def test_edit_album_info(self):
        response = self.client.post(reverse('album_list'), self.data_album)
        album_id = response.data['id']
        self.edit_album = {
            "name": "两行诗",
            "release_time": "2008-08-17 22:12:01",
            "is_show": True,
            "related_account": self.test_user.id
        }
        res = self.client.patch(reverse('album_modify', kwargs={'pk': album_id}), data=self.edit_album)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], self.edit_album['name'])
        self.assertEqual(res.data['release_time'], self.edit_album['release_time'])
        self.assertEqual(res.data['is_show'], self.edit_album['is_show'])
        self.assertEqual(res.data['related_account'], self.test_user.id)
        self.assertEqual(res.data['nick_name'], self.nick_name)

    def test_get_all_album_picture(self):
        picture_num = 10
        response = self.client.post(reverse('album_list'), self.data_album)
        album_id = response.data['id']
        for i in range(picture_num):
            AlbumPicture.objects.create(album_id=album_id, picture=self.data_picture[0])
        res = self.client.get(reverse('picture_list', kwargs={"album_id": album_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), picture_num)

    def test_add_picture_to_album(self):
        response = self.client.post(reverse('album_list'), self.data_album)
        album_id = response.data['id']
        res = self.client.post(reverse('picture_list', kwargs={"album_id": album_id}), data=json.dumps(self.data_picture), content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['saved'], 1)
