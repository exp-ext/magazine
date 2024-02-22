import django_filters
from outlets.models import Outlet


class OutletFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Outlet
        fields = ('title',)
