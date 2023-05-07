from django.core.cache import cache
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django_lifecycle import hook, AFTER_CREATE, AFTER_UPDATE, \
    LifecycleModelMixin

from project.mixins.models import PKMixin
from project.model_choices import FeedbackCacheKeys


class Feedback(LifecycleModelMixin, PKMixin):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    text = models.TextField(
        blank=True,
        null=True
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)],
    )

    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE)
    def after_signal(self):
        cache.delete(FeedbackCacheKeys.FEEDBACKS)
