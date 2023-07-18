from django.urls import path, include
from .views import ProductsView, ExportCSVView, ImportCSV, ProductDetail, \
    ProductByCategory
from favorites.urls import urlpatterns as favorites_urlpatterns


urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('<uuid:pk>', ProductDetail.as_view(), name='product'),
    path('export-csv/', ExportCSVView.as_view(), name='products_to_csv'),
    path('import-csv/', ImportCSV.as_view(), name='products_from_csv'),
    path('favorites/', include(favorites_urlpatterns)),
    path('<slug:slug>/', ProductByCategory.as_view(),
         name='products_by_category'),
]
