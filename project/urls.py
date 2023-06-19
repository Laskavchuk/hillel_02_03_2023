"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.permissions import IsAuthenticated

from products.urls import urlpatterns as products_urlpatterns
from django.conf import settings
from feedbacks.urls import urlpatterns as feedbacks_urlpatterns
from accounts.urls import urlpatterns as accounts_urlpatterns
from main.urls import urlpatterns as main_urlpatterns
from orders.urls import urlpatterns as orders_urlpatterns
from apis.products.urls import urlpatterns as api_products_urlpatterns
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

i18n_urlpatterns = [
    path('products/', include(products_urlpatterns)),
    path('feedbacks/', include(feedbacks_urlpatterns)),
    path('accounts/', include(accounts_urlpatterns)),
    path('', include(main_urlpatterns)),
    path('', include(orders_urlpatterns))
]
api_urlpatterns = [
    *api_products_urlpatterns
]
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_urlpatterns)),

]
schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v1',
        description="Test description",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=[IsAuthenticated],
)

urlpatterns_swagger = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]
urlpatterns = urlpatterns + i18n_patterns(*i18n_urlpatterns) + \
              urlpatterns_swagger

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]

if settings.DEBUG:
    urlpatterns += [
        path('silk/', include('silk.urls', namespace='silk')),
        path('__debug__/', include('debug_toolbar.urls')),
    ]