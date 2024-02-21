
from core.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from django_filters import rest_framework as filters
from rest_framework import viewsets
from warehouses.filters import WarehouseFilter
from warehouses.models import Warehouse
from warehouses.serializers import WarehouseSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = WarehouseSerializer
    queryset = Warehouse.objects.all()
    filterset_class = WarehouseFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
