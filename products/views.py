import csv

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, FormView
from .models import Product
from products.model_forms import ProductModelForm, ImportCSVForm


class ProductView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.iterator()
        context['form'] = ProductModelForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ProductModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        return self.render_to_response(self.get_context_data())


class ExportCSVView(View):
    def get(self, request, *args, **kwargs):
        headers = {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="products.csv"'
        }
        response = HttpResponse(headers=headers)
        fields_name = ['name', 'categories', 'description', 'sku', 'image', 'price', 'is_active']
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

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
