from rest_framework import status
from rest_framework.test import APITestCase

from biz.models import User


# 测试视频
video_url = "http://qa.bituquanguan.com/uploads/5b/df/f2d60475f18bf0d4a304351215b686a5fd4d.mp4"
video_size = int(537296 / 1024 / 1024)  # 单位：M
video_width = 960
video_height = 540


class GetVideoInfo(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(mobile='11111111111', password='password')
        self.client = self.client_class()
        self.client.login(username=self.test_user, password='password')

    def test_get_video_info(self):
        res = self.client.post('/video_resolution', data={"video_url": video_url})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['width'], video_width)
        self.assertEqual(res.data['height'], video_height)
        self.assertEqual(res.data['size'], video_size)
