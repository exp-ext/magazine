from django.urls import include, path
from rest_framework.routers import DefaultRouter
from outlets.views import OutletViewSet

router = DefaultRouter()
router.register('', OutletViewSet, basename='outlets')

urlpatterns = [
    path('', include(router.urls)),
]
