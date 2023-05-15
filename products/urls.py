from django.urls import path
from .views import ProductsView, ExportCSVView, ImportCSV, ProductDetail, \
    ProductByCategory

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('<uuid:pk>', ProductDetail.as_view(), name='product'),
    path('export-csv/', ExportCSVView.as_view(), name='products_to_csv'),
    path('import-csv/', ImportCSV.as_view(), name='products_from_csv'),
    path('<slug:slug>/', ProductByCategory.as_view(),
         name='products_by_category'),
]
