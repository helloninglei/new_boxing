from rest_framework import viewsets, mixins
from boxing_console.permissions import IsSuperAdminPermission
from biz.models import User
from boxing_console.serializers import AdminSerializer


class AdminViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin):
    permission_classes = (IsSuperAdminPermission,)
    queryset = User.objects.filter(is_active=True, is_staff=True).order_by("-date_joined")
    serializer_class = AdminSerializer

    def perform_destroy(self, instance):
        instance.is_staff = False
        instance.save()
