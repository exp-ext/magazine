from core.permissions import IsAdmin, IsModerator, IsOwner, ReadOnly
from django_filters import rest_framework as filters
from rest_framework import viewsets
from outlets.filters import OutletFilter
from outlets.models import Outlet
from outlets.serializers import OutletSerializer


class OutletViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner | IsModerator | IsAdmin | ReadOnly,)
    serializer_class = OutletSerializer
    queryset = Outlet.objects.all()
    filterset_class = OutletFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
