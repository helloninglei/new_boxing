from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from biz.models import Feedback
from boxing_app.serializers import FeedbackSerializer
from boxing_app.services.decorater import limit_success_frequency


class FeedbackViewSet(mixins.CreateModelMixin,
                      GenericViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    @limit_success_frequency(frequency=5, period=60*60*24)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
