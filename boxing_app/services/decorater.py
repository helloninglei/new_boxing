import functools

from rest_framework import status
from rest_framework.response import Response

import settings
from biz import constants
from biz.redis_client import redis_client


def limit_success_frequency(frequency, period):
    def decorater(func):
        @functools.wraps(func)
        def wrapper(viewset, request, *args, **kwargs):
            key = func.__module__ + "__" + func.__qualname__ + "__" + str(request.user.id)
            posted_frequency = redis_client.get(key)
            if posted_frequency and int(posted_frequency) >= frequency:
                return Response(data="24小时内只能提交5次反馈建议，请稍后再试", status=status.HTTP_429_TOO_MANY_REQUESTS)
            res = func(viewset, request, *args, **kwargs)
            if str(res.status_code)[0] != "2":
                return res
            frequency_incr = redis_client.incr(key)
            if frequency_incr == 1:
                if settings.ENVIRONMENT == settings.TEST:
                    period = constants.TEST_LIMIT_PERIOD_
                elif settings.ENVIRONMENT == settings.DEVELOPMENT:
                    period = constants.DEVELOPMENT_LIMIT_PERIOD
                redis_client.expire(key, period)
            return res
        return wrapper
    return decorater
