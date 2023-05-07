from django.db.models import IntegerChoices, TextChoices


class DiscountTypes(IntegerChoices):
    VALUE = 0, 'У грошах'
    PERCENT = 1, 'Відсотки'


class Currencies(TextChoices):
    UAH = 'UAH', 'UAH'
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'


class ProductCacheKeys(TextChoices):
    PRODUCTS = 'products', 'Products all'


class FeedbackCacheKeys(TextChoices):
    FEEDBACKS = 'feedbacks', 'Feedbacks all'
