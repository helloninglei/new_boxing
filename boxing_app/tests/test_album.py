# -*- coding:utf-8 -*-
from biz.models import User
from biz.models import UserProfile
from biz.models import Album
from biz.models import AlbumPicture
from django.urls import reverse
from rest_framework.test import APITestCase
from django.utils import timezone


class AlbumTestCase(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(mobile='11111111111', password='password')
        self.nick_name = '膜法师'
        UserProfile.objects.filter(user=self.test_user).update(nick_name='膜法师')
        self.client = self.client_class()

    def test_album_list(self):
        album = Album.objects.create(name='他',
                                     release_time=timezone.now(),
                                     is_show=True,
                                     related_account_id=self.test_user.id)
        res = self.client.get(reverse('album_list', kwargs={'pk': self.test_user.id}))
        self.assertEqual(res.data['results'][0]['id'], album.id)
        self.assertEqual(res.data['results'][0]['name'], '他')

    def test_album_detail(self):
        album = Album.objects.create(name='为长者续1秒',
                                     release_time=timezone.now(),
                                     is_show=True,
                                     related_account_id=self.test_user.id)
        pic = AlbumPicture.objects.create(picture='/path/to/pic.jog',
                                          created_time=timezone.now(),
                                          album=album)
        res = self.client.get(reverse('picture_list', kwargs={'pk': album.id}))
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['picture'], pic.picture)
        self.assertEqual(res.data['results'][0]['id'], pic.id)

    def test_user_profile_has_album(self):
        res = self.client.get(reverse('user-profile', kwargs={'pk': self.test_user.id}))
        self.assertEqual(res.data['has_album'], False)
        Album.objects.create(name='沟里锅架绳四倚',
                             release_time=timezone.now(),
                             is_show=True,
                             related_account_id=self.test_user.id)
        res = self.client.get(reverse('user-profile', kwargs={'pk': self.test_user.id}))
        self.assertEqual(res.data['has_album'], True)
