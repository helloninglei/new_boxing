from django.db.models import Q, Count
from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet

from biz.constants import PAYMENT_STATUS_PAID
from biz.models import Message, GameNews, HotVideo, UserProfile
from biz.redis_client import blocked_user_list
from biz.utils import comment_count_condition
from boxing_app.serializers import MessageSerializer, NewsSerializer, HotVideoSerializer, \
    UserProfileSerializer


class SearchVewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        search_type = kwargs['search_type']
        keywords = self.request.query_params.get('keywords')
        if search_type == "USER":
            self.serializer_class = UserProfileSerializer
            qs = UserProfile.objects.filter(nick_name__icontains=keywords) \
                .select_related("user", "user__boxer_identification")\
                .order_by('-created_time')
            self.queryset = qs if keywords else []
        elif search_type == "MESSAGE":
            user_id = self.request.user.id
            blocked_user_id_list = blocked_user_list(user_id)
            is_like = Count('likes', filter=Q(likes__user_id=user_id), distinct=True)
            self.serializer_class = MessageSerializer
            qs = Message.objects.filter(content__icontains=keywords) \
                .exclude(user_id__in=blocked_user_id_list) \
                .annotate(ike_count=Count('likes', distinct=True), comment_count=comment_count_condition,
                          is_like=is_like).select_related('user__boxer_identification', 'user__user_profile')
            self.queryset = qs if keywords else []
        elif search_type == "NEWS":
            self.serializer_class = NewsSerializer
            qs = GameNews.objects.filter(title__icontains=keywords) \
                .annotate(comment_count=comment_count_condition)
            self.queryset = qs if keywords else []
        elif search_type == "VIDEO":
            _filter = Q(orders__status=PAYMENT_STATUS_PAID, orders__user_id=self.request.user.id)
            self.serializer_class = HotVideoSerializer
            qs = HotVideo.objects.filter(Q(name__icontains=keywords) | Q(description__icontains=keywords)) \
                .annotate(is_paid=Count('orders', filter=_filter), comment_count=comment_count_condition)
            self.queryset = qs if keywords else []
        return super().list(request, *args, **kwargs)
