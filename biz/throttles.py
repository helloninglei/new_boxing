from rest_framework.throttling import UserRateThrottle


class FeedbackRateThrottle(UserRateThrottle):
    rate = '5/day'
