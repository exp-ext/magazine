from attributes.views import AttributeViewSet, UnitViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('units', UnitViewSet, basename='units')
router.register('attrs', AttributeViewSet, basename='attributes')

urlpatterns = [
    path('', include(router.urls)),
]
