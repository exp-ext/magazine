import django_filters
from addresses.models import Address


class AddressFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='street', lookup_expr='icontains')

    class Meta:
        model = Address
        fields = ('street',)
