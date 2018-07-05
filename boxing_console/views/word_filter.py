from rest_framework import viewsets
from biz.models import WordFilter
from boxing_console.serializers import WordFilterSerializer


class WordFilterViewSet(viewsets.ModelViewSet):
    queryset = WordFilter.objects.all().order_by("-updated_time")
    serializer_class = WordFilterSerializer
