from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

from project.mixins.models import PKMixin


class Feedback(PKMixin):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    text = models.TextField(
        blank=True,
        null=True
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)],
    )
