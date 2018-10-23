
from django.conf import settings


def get_cdn_url(url):
    return url if url.startswith("http") else f"{settings.CDN_BASE_URL}{url}"
