from .currency_checker import CurrencyChecker
from datetime import date
from typing import List, Optional
import requests


class GeoCurrencyChecker(CurrencyChecker):
    def __init__(self, api_key: str, base: str, target: str, **kwargs):
        super().__init__(base, target, **kwargs)

        self._api_key = api_key

    def get_exchange_rate(self,
                          amount: float = 1,
                          date: Optional[date] = None) -> float:
        parameters = {
            'api_key': self._api_key,
            'from': self._base,
            'to': self._target,
            'amount': amount,
            'format': 'json'
        }

        base_url = 'https://api.getgeoapi.com/v2/currency'
        if date:
            url = f'{base_url}/historical/{date.isoformat()}'
        else:
            url = f'{base_url}/convert'

        response = requests.get(url, parameters)
        response.raise_for_status()

        rate = float(response.json()['rates'][self._target]['rate_for_amount'])

        return rate

    def get_time_series(self, start: date, end: date) -> List[float]:
        raise NotImplementedError('The GeoAPI time series endpoint is not available')


if __name__ == '__main__':
    from argparse import ArgumentParser

    arg_parser = ArgumentParser()
    arg_parser.add_argument('api_key', type=str)

    args = arg_parser.parse_args()

    currency_checker = GeoCurrencyChecker(
        args.api_key, base='EUR', currency='KRW')

    rate_for_amount = currency_checker.get_exchange_rate()
    print(rate_for_amount)
