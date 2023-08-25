import requests
from .currency_checker import CurrencyChecker
from datetime import date
from typing import List, Optional


class FixerCurrencyChecker(CurrencyChecker):
    def __init__(self, api_key: str, base: str, currency: str, **kwargs):
        super().__init__(base, currency, **kwargs)

        self._access_key = api_key

    def get_exchange_rate(self, date: Optional[date] = None) -> float:
        base_url = 'http://data.fixer.io/api'

        if date:
            url = f'{base_url}/{date.isoformat()}'
        else:
            url = f'{base_url}/latest'

        parameters = {
            'access_key': self._access_key,
            'base': self._base,
            'symbols': self._currency
        }

        response = requests.get(url, parameters)
        response.raise_for_status()

        rate = response.json()['rates'][self._currency]

        return rate

    def get_time_series(self, start: date, end: date) -> List[float]:
        url = 'http://data.fixer.io/api/timeseries'

        parameters = {
            'access_key': self._access_key,
            'start_date': start.isoformat(),
            'end_date': end.isoformat(),
            'base': self._base,
            'symbols': self._currency
        }
        response = requests.get(url, parameters)
        response.raise_for_status()

        raise NotImplementedError


'''
time series response e.g.
{
    "success": true,
    "timeseries": true,
    "start_date": "2012-05-01",
    "end_date": "2012-05-03",
    "base": "EUR",
    "rates": {
        "2012-05-01":{
          "USD": 1.322891,
          "AUD": 1.278047,
          "CAD": 1.302303
        },
        "2012-05-02": {
          "USD": 1.315066,
          "AUD": 1.274202,
          "CAD": 1.299083
        },
        "2012-05-03": {
          "USD": 1.314491,
          "AUD": 1.280135,
          "CAD": 1.296868
        },
        [...]
    }
}
'''
