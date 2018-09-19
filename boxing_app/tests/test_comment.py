# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase
from rest_framework import status

from biz import constants
from biz.constants import PAYMENT_STATUS_PAID
from biz.models import User, Message, HotVideo, Comment, PayOrder


class CommentTestCase(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(mobile='11111111111', password='password')
        self.test_user_2 = User.objects.create_user(mobile='11111111112', password='password')
        self.client1 = self.client_class()
        self.client1.login(username=self.test_user_1, password='password')
        self.client2 = self.client_class()
        self.client2.login(username=self.test_user_2, password='password')
        self.anonymous_client = self.client_class()

    def prepare(self):
        res = self.client1.post('/messages', {'content': 'message1'})
        self.message_id = message_id = res.data['id']
        self.msg1 = msg1 = {'content': 'comment1 by user1'}
        self.msg2 = msg2 = {'content': 'comment2 by user2'}
        res1 = self.client1.post('/messages/%s/comments' % message_id, msg1)
        res2 = self.client2.post('/messages/%s/comments' % message_id, msg2)
        self.comment1 = res1.data
        self.comment2 = res2.data

    def test_create_comment(self):
        self.prepare()
        response = self.client1.get(path='/messages/%s/comments' % self.message_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        results = response.data['results']
        self.assertEqual(self.comment1['user']['id'], self.test_user_1.id)
        self.assertEqual(self.msg1['content'], results[1]['content'])
        self.assertEqual(self.comment2['user']['id'], self.test_user_2.id)
        self.assertEqual(self.msg2['content'], results[0]['content'])

        # has unread comment list
        response = self.client1.get(path="/unread_like_comment")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['has_unread_like'])
        self.assertTrue(response.data['has_unread_comment'])

        # read comment list
        response = self.client1.get(path="/comment_me")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # not has unread comment list
        response = self.client1.get(path="/unread_like_comment")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['has_unread_like'])
        self.assertFalse(response.data['has_unread_comment'])

    def test_reply(self):
        self.prepare()
        reply_data = {
            'content': 'reply to comment 1'
        }
        reply_to_reply_data = {
            'content': 'reply to reply 1'
        }
        res = self.client1.post('/messages/%s/comments/%s' % (self.message_id, self.comment1['id']), reply_data)
        reply_id = res.data['id']

        res = self.client2.post('/messages/%s/comments/%s' % (self.message_id, reply_id), reply_to_reply_data)
        reply_to_reply_id = res.data['id']

        res = self.client1.get(path='/messages/%s/comments' % self.message_id)
        comments = res.data['results']
        for comment in comments:
            if comment['id'] == self.comment1['id']:
                replies = comment['replies']
                self.assertEqual(len(replies), 2)
                for reply in replies['results']:
                    if reply['id'] == reply_id:
                        self.assertEqual(reply['content'], reply_data['content'])
                        self.assertEqual(reply['user']['id'], self.test_user_1.id)
                    if reply['id'] == reply_to_reply_id:
                        self.assertEqual(reply['content'], reply_to_reply_data['content'])
                        self.assertEqual(reply['user']['id'], self.test_user_2.id)
                        self.assertEqual(reply['to_user']['id'], self.test_user_1.id)

    def test_delete(self):
        self.prepare()

        res = self.client2.delete('/messages/%s/comments/%s' % (self.message_id, self.comment1['id']))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client1.delete('/messages/%s/comments/%s' % (self.message_id, self.comment1['id']))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client1.get('/messages/%s/comments' % self.message_id)
        self.assertEqual(len(response.data['results']), 1)

        reply_data = {
            'content': 'reply to comment 1'
        }
        reply_to_reply_data = {
            'content': 'reply to reply 1'
        }
        res = self.client1.post('/messages/%s/comments/%s' % (self.message_id, self.comment2['id']), reply_data)
        reply_id = res.data['id']

        res = self.client2.post('/messages/%s/comments/%s' % (self.message_id, reply_id), reply_to_reply_data)
        reply_to_reply_id = res.data['id']

        res = self.client2.delete('/messages/%s/comments/%s' % (self.message_id, reply_id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client1.delete('/messages/%s/comments/%s' % (self.message_id, reply_id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.client1.get('/messages/%s/comments' % self.message_id)
        comment = res.data['results'][0]
        replies = comment['replies']
        self.assertEqual(replies['count'], 1)
        reply = replies['results'][0]
        self.assertEqual(reply['id'], reply_to_reply_id)
        self.assertIsNotNone(reply['to_user'])

    def test_permission(self):
        self.prepare()
        res = self.anonymous_client.get(f'/messages/{self.message_id}/comments')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

        reply_data = {
            'content': 'reply to comment 1'
        }
        res = self.anonymous_client.post('/messages/%s/comments/%s' % (self.message_id, self.comment1['id']),
                                         reply_data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_me_for_message(self):
        self.prepare()
        res = self.client1.get('/comment_me')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

        comment_id = self.comment1['id']
        msg3 = {'content': 'comment by user2 to user1'}
        self.client2.post('/messages/%s/comments/%s' % (self.message_id, comment_id), msg3)
        res = self.client1.get('/comment_me')
        self.assertEqual(len(res.data['results']), 3)

        # if message is delete comment should not show in list
        message = Message.objects.get(id=self.message_id)
        message.soft_delete()
        message.save()
        res = self.client1.get('/comment_me')
        self.assertEqual(len(res.data['results']), 0)

        # test comment on hot_video
        hot_video_data = {
            'name': 'test video1',
            'description': 'test video1',
            'price': 111,
            'url': '/videos/111',
            'try_url': '/videos/222',
            'operator_id': self.test_user_1.id,
            'cover': '/videos/333',
            "push_hot_video": False,
            "tag": constants.HOT_VIDEO_TAG_DEFAULT,
        }

        video = HotVideo.objects.create(**hot_video_data)
        video.users.add(self.test_user_1.id)
        PayOrder.objects.create(**{
            "user": self.test_user_1,
            "content_type": ContentType.objects.get(app_label="biz", model="HotVideo"),
            "object_id": video.id,
            "status": PAYMENT_STATUS_PAID,
            "out_trade_no": 201809140001,
            "amount": 100,
            "device": constants.DEVICE_PLATFORM_IOS,
        })
        comment1 = Comment.objects.create(**{
            "content_type": ContentType.objects.get(app_label="biz", model="HotVideo"),
            "object_id": video.id,
            "content": "comment on video %s" % video.id,
            "user": self.test_user_1
        })
        Comment.objects.create(**{
            "content_type": ContentType.objects.get(app_label="biz", model="HotVideo"),
            "object_id": video.id,
            "content": "comment on video %s" % video.id,
            "user": self.test_user_2,
            "parent": comment1,
            "ancestor": comment1
        })
        res = self.client1.get('/comment_me')
        self.assertEqual(len(res.data['results']), 1)
        self.assertTrue(res.data['results'][0]['to_object']['is_paid'])

        # if video is hidden, comment should disappear
        video.is_show = False
        video.save()
        video.refresh_from_db()
        res = self.client1.get('/comment_me')
        self.assertEqual(len(res.data['results']), 0)


