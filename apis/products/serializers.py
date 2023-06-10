from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from products.models import Product, Category


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name')


class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'sku', 'created_at', 'updated_at',
                  'description', 'image', 'categories', 'category_name')

    def get_category_name(self, obj):
        return obj.categories.values_list('name', flat=True)


class ProductDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ()

    def validate(self, attrs):
        if self.instance.order_items.exists():
            raise ValidationError("Cannot delete some instances of model "
                                  "'Product' because they are referenced "
                                  "through protected foreign keys", )
        return attrs


class CategoryNameSerializer(serializers.Serializer):
    name = serializers.CharField()


class ProductCreateSerializer(serializers.ModelSerializer):
    category_names = serializers.ListSerializer(
        child=CategoryNameSerializer(),
        required=False,
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'sku', 'created_at', 'updated_at',
                  'description', 'image', 'categories', 'currency',
                  'is_active', 'category_names')
        read_only_fields = ('id', 'created_at', 'updated_at', 'image',
                            'categories')
        extra_kwargs = {
            "description": {
                "required": True,
                "allow_blank": False
            },
        }

    def validate_category_names(self, value):
        return Category.objects.filter(
            name__in=[i['name'] for i in value]
        ).values_list('id', flat=True)

    def validate(self, attrs):
        category_names = attrs.pop('category_names', None)
        if category_names:
            attrs['categories'] = category_names
        return attrs


class ProductSerializer(serializers.ModelSerializer):
    category_names = serializers.ListSerializer(
        child=CategoryNameSerializer(),
        required=False,
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'sku', 'created_at', 'updated_at',
                  'description', 'image', 'categories', 'currency',
                  'is_active', 'category_names')
        read_only_fields = ('id', 'created_at', 'updated_at', 'image',
                            'categories')
        extra_kwargs = {
            "description": {
                "required": True,
                "allow_blank": False
            },
        }

    def validate_category_names(self, value):
        return Category.objects.filter(
            name__in=[i['name'] for i in value]
        ).values_list('id', flat=True)

    def validate(self, attrs):
        category_names = attrs.pop('category_names', None)
        if category_names:
            attrs['categories'] = category_names
        return attrs
