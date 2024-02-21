import django_filters
from warehouses.models import Warehouse


class WarehouseFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название склада')

    class Meta:
        model = Warehouse
        fields = ('title',)
