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
from django.contrib import admin
from django.urls import path, include
from products.urls import urlpatterns as products_urlpatterns
from django.conf import settings
from feedbacks.urls import urlpatterns as feedbacks_urlpatterns
from accounts.urls import urlpatterns as accounts_urlpatterns
from main.urls import urlpatterns as main_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include(products_urlpatterns)),
    path('feedbacks/', include(feedbacks_urlpatterns)),
    path('accounts/', include(accounts_urlpatterns)),
    path('', include(main_urlpatterns))

]
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
