from django.urls import path
from .views import ProductView, ExportCSVView, ImportCSV
urlpatterns = [
    path('', ProductView.as_view(), name='products'),
    path('export-csv/', ExportCSVView.as_view(), name='products_to_csv'),
    path('import-csv/', ImportCSV.as_view(), name='products_from_csv'),
]
