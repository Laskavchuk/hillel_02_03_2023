from rest_framework import serializers

from products.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'sku', 'created_at', 'updated_at',
                  'description', 'image', 'categories', 'category_name',
                  'currency')

    def get_category_name(self, obj):
        return obj.categories.values_list('name', flat=True)
