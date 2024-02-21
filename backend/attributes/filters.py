import django_filters
from attributes.models import Attribute


class AttributeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Attribute
        fields = ('name',)
