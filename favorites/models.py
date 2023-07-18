from django.contrib.auth import get_user_model
from django.db import models

from project.mixins.models import PKMixin


class Favorite(PKMixin):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('user', 'product')
