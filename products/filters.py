from datetime import timedelta

import django_filters
from django.utils import timezone

from products.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    sku = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.RangeFilter()
    date = django_filters.DateFromToRangeFilter(field_name='created_at')
    new = django_filters.BooleanFilter(method='get_new')

    class Meta:
        model = Product
        fields = ['price', 'name', 'sku', 'date', 'new']

    def get_new(self, qs, name, value):
        if value:
            return qs.filter(created_at__gt=timezone.now() - timedelta(days=1))
        return qs
