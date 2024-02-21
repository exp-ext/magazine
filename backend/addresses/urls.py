from django.urls import include, path
from addresses.views import (AddressViewSet, CityViewSet, CountryViewSet,
                             RegionViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('addresses', AddressViewSet, basename='addresses')
router.register('cities', CityViewSet, basename='cities')
router.register('countries', CountryViewSet, basename='countries')
router.register('regions', RegionViewSet, basename='regions')


urlpatterns = [
    path('', include(router.urls)),
]
