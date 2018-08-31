from django.conf import settings
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


def get_captcha():
    key = CaptchaStore.generate_key()
    data = {
        "captcha_hash": key,
        "url": captcha_image_url(key)
    }
    return data


def check_captcha(captcha_code, captcha_hash):
    """
    :param captcha_code: 用户输入的验证码
    :param captcha_hash: 验证码的hash key
    :return: bool
    """
    CaptchaStore.remove_expired()

    if CaptchaStore.objects.filter(response=captcha_code, hashkey=captcha_hash).exists():
        CaptchaStore.objects.filter(response=captcha_code, hashkey=captcha_hash).delete()
        return True

    if settings.ENVIRONMENT == settings.DEVELOPMENT:
        return True

    return False
