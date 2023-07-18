import decimal

from django.db import models

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from project.model_choices import Currencies


class CurrencyHistory(PKMixin):
    code = models.CharField(
        max_length=16,
        choices=Currencies.choices,
        default=Currencies.UAH
    )
    buy = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )
    sale = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )

    def __str__(self):
        return f"{self.code} - {self.buy}/ {self.sale}"

    @classmethod
    def last_curs(cls, code, attr='sale'):
        return getattr(cls.objects.filter(
            code=code
        ).order_by('-created_at').first(), attr, decimal.Decimal('1.00'))
