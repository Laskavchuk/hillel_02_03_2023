from currencies.clients.monobank import monobank_client
from currencies.clients.privatbank import privatbank_client


class CurrencyApiClient:
    def __init__(self):
        self.monobank_client = monobank_client
        self.privatbank_client = privatbank_client

    def save_data(self):
        if self.privatbank_client.has_data():
            self.privatbank_client.save()
        else:
            self.monobank_client.save()


currency_api_client = CurrencyApiClient()
