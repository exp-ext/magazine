from django.urls import include, path
from rest_framework.routers import DefaultRouter
from warehouses.views import WarehouseViewSet

router = DefaultRouter()
router.register('', WarehouseViewSet, basename='warehouses')

urlpatterns = [
    path('', include(router.urls)),
]
