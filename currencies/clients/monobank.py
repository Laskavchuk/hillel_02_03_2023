from currencies.models import CurrencyHistory
from project.api_base_client import APIBaseClient


class Mononbank(APIBaseClient):
    base_url = 'https://api.monobank.ua/bank/currency'

    def _prepare_data(self):
        self._request(
            'get',
        )
        results = []
        if self.response:
            for obj in self.response.json()[:2]:
                obj['currencyCodeA'] = 'USD' if obj['currencyCodeA'] == 840 \
                    else 'EUR'
                results.append({
                    'code': obj['currencyCodeA'],
                    'buy': obj['rateBuy'],
                    'sale': obj['rateSell']
                })
        return results

    def save(self):
        results = []
        for i in self._prepare_data():
            results.append(
                CurrencyHistory(
                    **i
                )
            )
        if results:
            CurrencyHistory.objects.bulk_create(results)


monobank_client = Mononbank()
