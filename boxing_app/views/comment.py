# -*- coding: utf-8 -*-
from django.db.models import Count, Avg, Q
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.fields import ContentType
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from biz import models
from biz.models import OrderComment, Comment
from biz.utils import get_model_class_by_name
from boxing_app.permissions import OnlyOwnerCanDeletePermission
from boxing_app.serializers import CommentSerializer, OrderCommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (OnlyOwnerCanDeletePermission, IsAuthenticatedOrReadOnly)
    serializer_class = CommentSerializer

    @property
    def content_object(self):
        object_class = get_model_class_by_name(self.kwargs['object_type'])
        return get_object_or_404(object_class, pk=self.kwargs['object_id'])

    def get_queryset(self):
        return self.content_object.comments.filter(parent=None).prefetch_related('user', 'user__boxer_identification')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        comment_count = 0
        for comment in response.data['results']:
            comment_count += 1
            comment_count += comment['replies']['count']
        response.data['comment_count'] = comment_count
        return response

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user,
            'content_object': self.content_object,
        }
        serializer.save(**kwargs)


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
        serializer.save(**kwargs)


class CourseCommentsAboutBoxer(viewsets.ReadOnlyModelViewSet):
    """与拳手相关的课程订单评论"""
    serializer_class = OrderCommentSerializer

    def get_queryset(self):
        boxer = models.BoxerIdentification.objects.filter(id=self.kwargs['boxer_id']).only('id').first()
        return OrderComment.objects.filter(order__course__boxer=boxer)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        count_and_avg_score = self.get_queryset().aggregate(count=Count('*'), avg_score=Avg("score"))
        response.data.update(count_and_avg_score)
        return response
