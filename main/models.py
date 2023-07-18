from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get(pk=1)
        except ObjectDoesNotExist:
            return cls()


class Config(SingletonModel):
    contact_form_email = models.EmailField()

    def __str__(self):
        return f"Config object: {self.contact_form_email}"
