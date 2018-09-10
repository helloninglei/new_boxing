from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from biz.models import User, Feedback, UserProfile


class FeedbackTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(mobile='11111111111', password='password')
        self.user2 = User.objects.create_superuser(mobile='11111111112', password='password')
        self.client1 = self.client_class()
        self.client2 = self.client_class()
        self.client1.login(username=self.user1, password='password')
        self.client2.login(username=self.user2, password='password')
        self.feedback_data = {
            "user": self.user1,
            "content": "用户1提交了一条反馈意见",
            "images": ["image01.png", "image02.png"]
        }

    def test_get_feedback_list(self):
        feedback_count = 5
        Feedback.objects.bulk_create(Feedback(**self.feedback_data) for _ in range(feedback_count))
        res = self.client2.get(reverse('feedback_list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), feedback_count)

        # search by mobile
        res = self.client2.get(reverse('feedback_list'), data={'search': self.user1.mobile})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), feedback_count)
        res = self.client2.get(reverse('feedback_list'), data={'search': self.user2.mobile})
        self.assertEqual(len(res.data['results']), 0)

        # search by nick_name
        UserProfile.objects.filter(user=self.user1).update(nick_name="张三")
        UserProfile.objects.filter(user=self.user2).update(nick_name="张四")
        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        res = self.client2.get(reverse('feedback_list'), data={'search': self.user1.user_profile.nick_name})
        self.assertEqual(len(res.data['results']), feedback_count)
        res = self.client2.get(reverse('feedback_list'), data={'search': self.user2.user_profile.nick_name})
        self.assertEqual(len(res.data['results']), 0)




    def test_get_feedback_detail(self):
        fd = Feedback.objects.create(**self.feedback_data)
        res = self.client2.get(reverse('feedback_detail', kwargs={"pk": fd.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for key in self.feedback_data:
            if key == "user":
                self.assertEqual(res.data[key]['id'], self.user1.id)
            else:
                self.assertEqual(res.data[key], self.feedback_data[key])

    def test_do_mark(self):
        fd = Feedback.objects.create(**self.feedback_data)
        self.assertFalse(fd.mark)
        res = self.client2.post(reverse('do_mark', kwargs={"pk": fd.id, "operate": "mark"}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        fd = Feedback.objects.get(pk=fd.pk)
        fd.refresh_from_db()
        self.assertTrue(fd.mark)
        res = self.client2.post(reverse('do_mark', kwargs={"pk": fd.id, "operate": "unmark"}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        fd.refresh_from_db()
        self.assertFalse(fd.mark)

