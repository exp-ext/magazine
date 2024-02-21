from attributes.filters import AttributeFilter
from attributes.models import Attribute, Unit
from attributes.serializers import AttributeSerializer, UnitSerializer
from core.permissions import IsAdminOrReadOnly, IsModeratorOrReadOnly
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated


class UnitViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly | IsModeratorOrReadOnly,)
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('name',)


class AttributeViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AttributeSerializer
    queryset = Attribute.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AttributeFilter
