from os import path

from django.core.cache import cache
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django_lifecycle import hook, AFTER_CREATE, AFTER_UPDATE, \
    LifecycleModelMixin, BEFORE_UPDATE, BEFORE_CREATE

from currencies.models import CurrencyHistory
from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from project.model_choices import Currencies, ProductCacheKeys


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f'products/images/{str(instance.pk)}{extension}'


class Category(LifecycleModelMixin, PKMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    is_manual_slug = models.BooleanField(default=False)
    description = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to=upload_to,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name}"

    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when='name', has_changed=True)
    def after_signal(self):
        if not self.is_manual_slug:
            self.slug = slugify(self.name)


class Product(LifecycleModelMixin, PKMixin):
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
    categories = models.ManyToManyField(Category, blank=True)
    products = models.ManyToManyField("products.Product", blank=True)
    currency = models.CharField(
        max_length=16,
        choices=Currencies.choices,
        default=Currencies.UAH
    )

    def __str__(self):
        return f"{self.name} - {self.price}"

    def calculate_price(self):
        exchange_price = round(self.price * self.curs, 2)
        return exchange_price

    @property
    def curs(self):
        return CurrencyHistory.last_curs(self.currency)

    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE)
    def after_signal(self):
        cache.delete(ProductCacheKeys.PRODUCTS)
