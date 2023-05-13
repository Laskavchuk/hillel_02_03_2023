import csv
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.cache import cache
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, ListView

from project.model_choices import ProductCacheKeys
from .models import Product
from products.model_forms import ImportCSVForm


class ProductsView(ListView):
    context_object_name = 'products'
    model = Product

    def get_queryset(self):
        queryset = cache.get(ProductCacheKeys.PRODUCTS)
        if not queryset:
            print('TO CACHE')
            queryset = Product.objects.all()
            cache.set(ProductCacheKeys.PRODUCTS, queryset)

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


class ExportCSVView(View):
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        headers = {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="products.csv"'
        }
        response = HttpResponse(headers=headers)
        fields_name = ['name', 'categories', 'description',
                       'sku', 'image', 'price', 'is_active'
                       ]
        writer = csv.DictWriter(response, fieldnames=fields_name)
        writer.writeheader()
        for product in Product.objects.iterator():
            categories = ','.join([category.name for category in
                                   product.categories.all()]) or 'None'
            writer.writerow(
                {
                    'name': product.name,
                    'categories': categories,
                    'description': product.description,
                    'image': product.image.name if product.image else 'no image',
                    'sku': product.sku,
                    'price': product.price,
                    'is_active': product.is_active
                }
            )
        return response


class ImportCSV(FormView):
    form_class = ImportCSVForm
    template_name = 'products/import_csv.html'
    success_url = reverse_lazy('products')

    @method_decorator(login_required())
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
