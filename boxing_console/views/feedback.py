from rest_framework import status, mixins, filters
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from biz.models import Feedback
from boxing_console.serializers import FeedbackSerializer


class FeedbackViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ("user__mobile", "user__user_profile__nick_name")


    def do_mark(self, request, *args, **kwargs):
        mark = True if self.kwargs.get('operate') == "mark" else False
        Feedback.objects.filter(id=self.kwargs.get('pk')).update(mark=mark)
        return Response(status=status.HTTP_200_OK)
