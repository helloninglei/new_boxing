from rest_framework.test import APITestCase
from rest_framework import status
from biz.models import User, WordFilter


class WordFilterTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(mobile="19890000009", password="password")
        self.client = self.client_class()
        self.client.login(username=self.user.mobile, password="password")

    def test_list(self):
        WordFilter.objects.bulk_create([WordFilter(sensitive_word=f"_word{i}") for i in range(11)])
        response = self.client.get(path="/word_filters/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 11)
        self.assertEqual(response.data['next'], "http://testserver/word_filters/?page=2")
        self.assertEqual(len(response.data['results']), 10)

        WordFilter.objects.create(sensitive_word="name")
        response = self.client.get(path="/word_filters/", data={"search": "na"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['sensitive_word'], "name")

    def test_create_word_filter(self):
        response = self.client.post(path="/word_filters/", data={"sensitive_word": "hello"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sensitive_word'], "hello")

    def test_update_word_filter(self):
        word_filter = WordFilter.objects.create(sensitive_word="_word")
        self.assertEqual(word_filter.sensitive_word, "_word")
        response = self.client.put(path=f"/word_filters/{word_filter.id}/", data={"sensitive_word": "hello"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['sensitive_word'], "hello")

    def test_delete_word_filter(self):
        word_filter = WordFilter.objects.create(sensitive_word="_word")
        response = self.client.delete(path=f"/word_filters/{word_filter.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WordFilter.objects.filter(pk=word_filter.id).exists())
