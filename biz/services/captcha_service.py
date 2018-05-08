
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


def get_captcha():
    key = CaptchaStore.generate_key()
    data = {
        "captcha_hash": key,
        "url": captcha_image_url(key)
    }
    return data
