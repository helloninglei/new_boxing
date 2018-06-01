from rest_framework import mixins, viewsets
from django.db.models import Sum
from biz.models import OfficialAccountChangeLog
from boxing_console.serializers import OfficialAccountChangeLogsSerializer


class OfficialAccountChangeLogsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = OfficialAccountChangeLog.objects.all()
    serializer_class = OfficialAccountChangeLogsSerializer

    def list(self, request, *args, **kwargs):
        response = super(OfficialAccountChangeLogsViewSet, self).list(request, *args, **kwargs)
        total_count = self.queryset.aggregate(total_count=Sum("change_amount"))
        response.data.update(total_count)
        return response
