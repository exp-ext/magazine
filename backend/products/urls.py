from django.urls import include, path
from products.views import (BrandViewSet, ManufacturerViewSet,
                            ProductsCategoryViewSet, ProductViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', ProductViewSet, basename='warehouses')
router.register('', BrandViewSet, basename='brands')
router.register('', ProductsCategoryViewSet, basename='product-categories')
router.register('', ManufacturerViewSet, basename='manufacturers')

urlpatterns = [
    path('', include(router.urls)),
]
