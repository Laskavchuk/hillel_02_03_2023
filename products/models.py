from os import path

from django.db import models
from django.core.validators import MinValueValidator

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f'products/images/{str(instance.pk)}{extension}'


class Product(PKMixin):
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES)
    description = models.TextField(
        blank=True,
        null=True
    )
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to=upload_to,
        null=True,
        blank=True
    )


class Category(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to=upload_to,
        null=True,
        blank=True
    )


class Discount(models.Model):
    amount = models.PositiveIntegerField()
    code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    discount_type = models.IntegerField(
        choices=((0, 'У грошах'), (1, 'Відсотки')), default=0)
