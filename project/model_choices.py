from django.db.models import IntegerChoices


class DiscountTypes(IntegerChoices):
    VALUE = 0, 'У грошах'
    PERCENT = 1, 'Відсотки'