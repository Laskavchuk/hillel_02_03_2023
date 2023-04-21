from django.urls import path
from .views import ProductView, ExportCSVView, ImportCSV
from django.contrib.auth.decorators import login_required, user_passes_test
urlpatterns = [
    path('', ProductView.as_view(), name='products'),
    path('export-csv/', ExportCSVView.as_view(), name='products_to_csv'),
    path('import-csv/', login_required(ImportCSV.as_view()),
         name='products_from_csv'),
]
