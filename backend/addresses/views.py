from addresses.filters import AddressFilter
from addresses.models import Address, City, Country, Region
from addresses.serializers import (AddressSerializer, CitySerializer,
                                   CountrySerializer, RegionSerializer)
from core.permissions import IsAdmin, IsOwner, ReadOnly
from django_filters import rest_framework as filters
from rest_framework import viewsets


class CityViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin | ReadOnly,)
    serializer_class = CitySerializer
    queryset = City.objects.all()


class CountryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin | ReadOnly,)
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class RegionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin | ReadOnly,)
    serializer_class = RegionSerializer
    queryset = Region.objects.all()


class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner | IsAdmin | ReadOnly,)
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AddressFilter
