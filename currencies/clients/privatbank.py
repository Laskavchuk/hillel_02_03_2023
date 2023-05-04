from currencies.models import CurrencyHistory
from project.api_base_client import APIBaseClient


class PrivatBank(APIBaseClient):
    base_url = 'https://api.privatbank.ua/p24api/pubinfo'

    def _prepare_data(self):
        self._request(
            'get',
            params={
                'json': '',
                'exchange': '',
                'coursid': 5

            }
        )
        results = []
        if self.response:
            for i in self.response.json():
                results.append({
                    'code': i['ccy'],
                    'buy': i['buy'],
                    'sale': i['sale'],
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

    def has_data(self):
        data = self._prepare_data()
        return bool(data)


privatbank_client = PrivatBank()
    