"""
URL configuration for magazine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularJSONAPIView,
                                   SpectacularRedocView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api/v1/',
        include(
            [
                path('schema/', SpectacularAPIView.as_view(api_version='v1'), name='schema'),
                path('schema_json/', SpectacularJSONAPIView.as_view(api_version='v1'), name='schema_json'),
                path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

                path('users/', include(('users.urls', 'users'))),
                path('auth/', include('djoser.urls.authtoken')),
                path('addresses/', include(('addresses.urls', 'addresses'))),
                path('attributes/', include(('attributes.urls', 'attributes'))),
                # path('fileflow/', include(('fileflow.urls', 'fileflow'))),
                # path('outlets/', include(('outlets.urls', 'outlets'))),
                # path('products/', include(('products.urls', 'products'))),
                path('warehouses/', include(('warehouses.urls', 'warehouses'))),
            ]
        ),
    ),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
