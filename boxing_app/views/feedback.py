from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from biz.models import Feedback
from boxing_app.serializers import FeedbackSerializer


class FeedbackViewSet(mixins.CreateModelMixin,
                      GenericViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
