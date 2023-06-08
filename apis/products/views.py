from rest_framework import generics
from rest_framework.permissions import AllowAny

from apis.products.serializers import ProductListSerializer
from products.models import Product


class ProductList(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('categories').all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]


class ProductRetrieve(generics.RetrieveAPIView):
    queryset = Product.objects.prefetch_related('categories').all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
