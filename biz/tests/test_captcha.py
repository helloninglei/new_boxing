import unittest
from captcha.models import CaptchaStore
from biz.services.captcha_service import get_captcha, check_captcha


# 该单元测试需要使用boxing_app.app_settings
class CaptchaTEstCase(unittest.TestCase):
    def setUp(self):
        self.captcha_key = get_captcha()['captcha_hash']

    def test_get_captcha(self):
        self.assertTrue(CaptchaStore.objects.filter(hashkey=self.captcha_key).exists())

    def test_check_captcha(self):
        self.assertFalse(check_captcha("error_code", self.captcha_key))
        captcha_code = CaptchaStore.objects.filter(hashkey=self.captcha_key).first().response
        self.assertTrue(check_captcha(captcha_code, self.captcha_key))
