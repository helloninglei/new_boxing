import functools

from rest_framework import status
from rest_framework.response import Response

from biz.redis_client import redis_client


def limit_success_frequency(frequency, period, err_message):
    def decorater(func):
        @functools.wraps(func)
        def wrapper(viewset, request, *args, **kwargs):
            key = f"{func.__module__}__{func.__qualname__}__{request.user.id}"
            posted_frequency = redis_client.get(key)
            if posted_frequency and int(posted_frequency) >= frequency:
                return Response(data=err_message, status=status.HTTP_429_TOO_MANY_REQUESTS)
            res = func(viewset, request, *args, **kwargs)
            if str(res.status_code)[0] != "2":
                return res
            frequency_incr = redis_client.incr(key)
            if frequency_incr == 1:
                redis_client.expire(key, period)
            return res
        return wrapper
    return decorater
