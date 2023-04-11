from django import forms
from django.core.exceptions import ValidationError

from products.models import Product
from project.constants import MAX_DIGITS, DECIMAL_PLACES


class ProductForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    sku = forms.CharField()
    price = forms.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    image = forms.ImageField()

    def is_valid(self):
        is_valid = super().is_valid()
        if is_valid:
            try:
                Product.objects.get(name=self.cleaned_data['name'])
                is_valid = False
            except Product.DoesNotExist:
                ...
        return is_valid

    def save(self):
        return Product.objects.create(**self.cleaned_data)


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'sku', 'image', 'price')

    def clean_name(self):
        try:
            Product.objects.get(name=self.cleaned_data['name'])
            raise ValidationError('Product already exist.')
        except Product.DoesNotExist:
            ...
        return self.cleaned_data['name']