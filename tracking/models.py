from django.db import models

from project.mixins.models import PKMixin


class Tracking(PKMixin):
    method = models.CharField(max_length=16)
    url = models.CharField(max_length=255)
    data = models.JSONField(default=dict)
