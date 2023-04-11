from django.views.generic import TemplateView
from .models import Product
from products.model_forms import ProductModelForm


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

