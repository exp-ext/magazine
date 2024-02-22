from core.permissions import IsAdmin, IsModerator, IsOwner, ReadOnly
from django_filters import rest_framework as filters
from products.filters import ProductFilter
from products.models import Brand, Manufacturer, Product, ProductsCategory
from products.serializers import (BrandSerializer, ManufacturerSerializer,
                                  ProductsCategorySerializer,
                                  ProductSerializer)
from rest_framework import viewsets


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner | IsModerator | IsAdmin | ReadOnly,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filterset_class = ProductFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductsCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner | IsModerator | IsAdmin | ReadOnly,)
    serializer_class = ProductsCategorySerializer
    queryset = ProductsCategory.objects.all()


class ManufacturerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner | IsModerator | IsAdmin | ReadOnly,)
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()


class BrandViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner | IsModerator | IsAdmin | ReadOnly,)
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
