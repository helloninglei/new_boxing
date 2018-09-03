from django.db.models import Q, Count
from rest_framework import permissions, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from biz.constants import PAYMENT_STATUS_PAID
from biz.models import HotVideo, UserProfile
from biz.utils import comment_count_condition
from boxing_app.serializers import HotVideoSerializer, UserProfileSerializer
from boxing_app.views.game_news import NewsViewSet
from boxing_app.views.message import MessageViewSet


class SearchVewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = (permissions.AllowAny,)

    def search_user(self, request, *args, **kwargs):
        keywords = self.request.query_params.get('keywords', "")
        add_q = UserProfile.objects.none()
        if keywords == "徐晓冬":
            add_q = UserProfile.objects.filter(user__mobile=13501224847)  # 徐晓冬手机号
        qs = UserProfile.objects.filter(nick_name__icontains=keywords) \
            .select_related("user", "user__boxer_identification")\
            .order_by('-follower_count', 'created_time')
        self.serializer_class = UserProfileSerializer
        self.queryset = (add_q | qs) if keywords else []
        return super().list(request, *args, **kwargs)

    def search_video(self, request, *args, **kwargs):
        keywords = self.request.query_params.get('keywords', "")
        _filter = Q(orders__status=PAYMENT_STATUS_PAID, orders__user_id=self.request.user.id)
        qs = HotVideo.objects.filter(Q(is_show=True) & Q(name__icontains=keywords)) \
            .annotate(is_paid=Count('orders', filter=_filter), comment_count=comment_count_condition)
        self.serializer_class = HotVideoSerializer
        self.queryset = qs if keywords else []
        return super().list(request, *args, **kwargs)

    def search_all(self, request, *args, **kwargs):
        user_list = self.search_user(request, *args, **kwargs).data['results'][:3]
        video_list = self.search_video(request, *args, **kwargs).data['results'][:3]
        message_list = MessageViewSet.as_view({"get": "search_message"})(self.request._request, *args, **kwargs).data['results'][:3]
        news_list = NewsViewSet.as_view({"get": "search_news"})(self.request._request, *args, **kwargs).data['results'][:3]
        return Response({"user_list": user_list, "video_list": video_list,
                         "message_list": message_list, "news_list": news_list})
