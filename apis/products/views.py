from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny

from apis.products.serializers import ProductListSerializer, \
    ProductDetailSerializer, ProductDeleteSerializer, ProductCreateSerializer,\
    ProductSerializer
from products.models import Product


class ProductList(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('categories').all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]


class ProductRetrieve(generics.RetrieveAPIView):
    queryset = Product.objects.prefetch_related('categories').all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]


class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDeleteSerializer
    permission_classes = [AllowAny]

    def perform_destroy(self, instance):
        serializer = self.get_serializer(instance, data={})
        serializer.is_valid(raise_exception=True)
        instance.delete()


class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        serializer = ProductDeleteSerializer(instance, data={})
        serializer.is_valid(raise_exception=True)
        instance.delete()
