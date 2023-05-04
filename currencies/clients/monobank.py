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
            first_object = self.response.json()[0]
            first_object['currencyCodeA'] = 'USD'
            second_object = self.response.json()[1]
            second_object['currencyCodeA'] = 'EUR'
            results.append({
                'code': first_object["currencyCodeA"],
                'buy': first_object['rateBuy'],
                'sale': first_object['rateSell'],
            })
            results.append({
                'code': second_object["currencyCodeA"],
                'buy': second_object['rateBuy'],
                'sale': second_object['rateSell'],
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
