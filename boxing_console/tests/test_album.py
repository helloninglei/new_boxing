# -*- coding:utf-8 -*-

from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User
from biz.models import UserProfile


class AlbumTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_superuser(mobile='11111111111', password='password')
        UserProfile.objects.filter(user=self.test_user).update(nick_name='膜法师')
        self.client = self.client_class()
        self.client.login(username=self.test_user, password='password')
        self.data_album = {"name": "他改变了中国", "release_time": "1926-08-17 20:12:01",
                           "is_show": False, "related_account": self.test_user.id}
        self.data_picture = {"picture": "/uploads/52/a9/a96d7356a482ecc732c8b1f67b372717fb80.jpg"}

    def test_create_album(self):
        res = self.client.post('/album', self.data_album)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], '他改变了中国')
        self.assertEqual(res.data['release_time'], "1926-08-17 20:12:01")
        self.assertFalse(res.data['is_show'])
        self.assertEqual(res.data['related_account'], self.test_user.id)
        self.assertEqual(res.data['nick_name'], '膜法师')

    def test_get_album_list(self):
        album_count = 15
        for i in range(album_count):
            self.client.post('/album', self.data_album)
        res = self.client.get('/album')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], album_count)
        self.assertIsNotNone(res.data['next'])
        self.assertIsNone(res.data['previous'])
        self.assertEqual(len(res.data['results']), 10)

    def test_get_album_info(self):
        response = self.client.post('/album', self.data_album)
        album_id = response.data['id']
        res = self.client.get('/album/{}'.format(album_id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], '他改变了中国')
        self.assertEqual(res.data['release_time'], "1926-08-17 20:12:01")
        self.assertFalse(res.data['is_show'])
        self.assertEqual(res.data['related_account'], self.test_user.id)
        self.assertEqual(res.data['nick_name'], '膜法师')

    def test_edit_album_info(self):
        response = self.client.post('/album', self.data_album)
        album_id = response.data['id']
        self.edit_album = {
            "name": "两行诗",
            "release_time": "2008-08-17 22:12:01",
            "is_show": True,
            "related_account": self.test_user.id
        }
        res = self.client.patch('/album/{}'.format(album_id), data=self.edit_album)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], '两行诗')
        self.assertEqual(res.data['release_time'], "2008-08-17 22:12:01")
        self.assertTrue(res.data['is_show'])
        self.assertEqual(res.data['related_account'], self.test_user.id)
        self.assertEqual(res.data['nick_name'], '膜法师')

    def test_get_all_album_picture(self):
        picture_num = 10
        response = self.client.post('/album', self.data_album)
        album_id = response.data['id']
        for i in range(picture_num):
            self.client.post('/{}/picture'.format(album_id), data=self.data_picture)
        res = self.client.get('/{}/picture'.format(album_id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), picture_num)

    def test_add_picture_to_album(self):
        response = self.client.post('/album', self.data_album)
        album_id = response.data['id']
        res = self.client.post('/{}/picture'.format(album_id), data=self.data_picture)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(res.data)

    def test_delete_picture(self):
        response = self.client.post('/album', self.data_album)
        album_id = response.data['id']
        response = self.client.post('/{}/picture'.format(album_id), data=self.data_picture)
        picture_id = int(response.data)
        res = self.client.delete('/picture/{}'.format(picture_id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
