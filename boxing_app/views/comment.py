# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Avg, Q
from rest_framework import status, permissions, mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from biz import models
from biz.models import OrderComment, Message, HotVideo
from biz.utils import get_model_class_by_name, get_object_or_404, Round
from boxing_app.permissions import OnlyOwnerCanDeletePermission
from boxing_app.serializers import CommentSerializer, OrderCommentSerializer, CommentMeSerializer
from biz.easemob_client import EaseMobClient
from biz.redis_client import redis_client
from biz.redis_const import UNREAD_COMMENT


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (OnlyOwnerCanDeletePermission, IsAuthenticatedOrReadOnly)
    serializer_class = CommentSerializer

    @property
    def content_object(self):
        object_class = get_model_class_by_name(self.kwargs['object_type'])
        query_set = object_class.objects.all()
        if hasattr(object_class, 'is_show'):
            query_set = query_set.filter(is_show=True)
        return get_object_or_404(query_set, pk=self.kwargs['object_id'])

    def get_queryset(self):
        return self.content_object.comments.filter(parent=None).prefetch_related('user', 'user__boxer_identification')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['comment_count'] = self.content_object.comments.filter(Q(is_deleted=False) & (
                Q(ancestor__is_deleted=False) | Q(ancestor__isnull=True))).count()
        return response

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user,
            'content_object': self.content_object,
        }
        instance = serializer.save(**kwargs)
        if isinstance(instance.content_object, Message):
            EaseMobClient.send_passthrough_message([instance.content_object.user.id], msg_type="comment")
            redis_client.lpush(UNREAD_COMMENT.format(user_id=instance.content_object.user.id), instance.id)


class CommentMeListViewSet(mixins.ListModelMixin,
                           GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentMeSerializer

    def list(self, request, *args, **kwargs):
        message_content_type = ContentType.objects.get(app_label="biz", model="Message")
        video_content_type = ContentType.objects.get(app_label="biz", model="HotVideo")
        deleted_message = Message.all_objects.filter(is_deleted=True).values_list('id', flat=True)
        hidden_video = HotVideo.objects.filter(is_show=False).values_list('id', flat=True)
        self.queryset = models.Comment.objects.filter(Q(parent__user=request.user) |
                                                      (Q(message__user=request.user) & Q(parent__isnull=True)))\
            .exclude(Q(content_type=message_content_type, object_id__in=deleted_message) |
                     Q(content_type=video_content_type, object_id__in=hidden_video))\
            .order_by('-created_time')
        redis_client.delete(UNREAD_COMMENT.format(user_id=request.user.id))
        return super().list(request, *args, **kwargs)


class ReplyViewSet(CommentViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(pk=self.kwargs['pk'])

    def destroy(self, request, *args, **kwargs):
        self.get_object().soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        obj = self.get_object()
        kwargs = {
            'user': self.request.user,
            'content_object': self.content_object,
            'parent': obj,
            'ancestor_id': obj.ancestor_id or obj.id,
        }
        instance = serializer.save(**kwargs)
        EaseMobClient.send_passthrough_message([instance.parent.user_id], msg_type="comment")
        redis_client.lpush(UNREAD_COMMENT.format(user_id=instance.parent.user_id), instance.id)


class CourseCommentsAboutBoxer(viewsets.ReadOnlyModelViewSet):
    """与拳手相关的课程订单评论"""
    serializer_class = OrderCommentSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        boxer = models.BoxerIdentification.objects.filter(id=self.kwargs['boxer_id']).only('id').first()
        return OrderComment.objects.filter(order__course__boxer=boxer).select_related("order")

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        count_and_avg_score = self.get_queryset().aggregate(count=Count('*'), avg_score=Round(Avg("score")))
        response.data.update(count_and_avg_score)
        return response
