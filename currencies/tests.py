from datetime import timedelta

import freezegun
from django.utils import timezone

from currencies.models import CurrencyHistory
from currencies.tasks import get_currencies_task


def test_currencies(currency_history_factory, mocker):
    privat_client = mocker.patch(
        'currencies.clients.privatbank.privatbank_client._prepare_data')
    assert privat_client.call_count == 0
    privat_client.return_value = [
        {'code': 'USD', "buy": "40.55000", "sale": "41.55000"},
        {'code': 'EUR', "buy": "41.00000", "sale": "42.55000"},
    ]
    old = timezone.now() - timedelta(minutes=10)
    with freezegun.freeze_time(old):
        currency_history_factory()
    assert CurrencyHistory.objects.filter(created_at__lte=old).exists()
    get_currencies_task()
    assert not CurrencyHistory.objects.filter(created_at__lte=old).exists()
    assert privat_client.call_count == 2
    for item in privat_client.return_value:
        assert CurrencyHistory.objects.filter(
            code=item['code'],
            buy=item['buy'],
            sale=item['sale'],
        ).exists()
