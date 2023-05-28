from bs4 import BeautifulSoup
import logging
import json


from project.api_base_client import APIBaseClient

logger = logging.getLogger(__name__)


class CDKeys(APIBaseClient):
    base_url = 'https://www.cdkeys.com/pc/games?platforms=Steam'

    def _prepare_data(self):
        self._request(
            'get'
        )
        results = []
        if self.response and self.response.status_code == 200:
            soup = BeautifulSoup(self.response.content, 'html.parser')
            for item in soup.find_all('li', class_='product-item'):
                try:
                    results.append({
                        'name': json.loads(item.get('data-impression'))['name'],
                        'price': item.find('div', class_='price-box price-final_price').find('span', class_='price-wrapper').get('data-price-amount'),
                        'image': item.find('img').get('src'),
                        'sku': json.loads(item.get('data-impression'))['id'],
                        'category': json.loads(item.get('data-impression'))['brand'],
                        'description': json.loads(item.get('data-impression'))['category'],
                        # json.loads(item.get('data-impression'))['currency']
                        'currency': 'USD'
                    })
                except Exception as err:
                    logger.error(err)
            return results
        return results

    def parse(self):
        return self._prepare_data()

    def get_image(self, url):
        self._request(
            'get',
            url=url
        )
        return self.response


parser_client = CDKeys()
    