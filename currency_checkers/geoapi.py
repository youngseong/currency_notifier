import requests


# TODO: generalize the function
def check_currency_rate(api_key: str, **kwargs):
    target_currency = kwargs.get('target_currency', 'EUR')

    parameters = {
        'api_key': api_key,
        'from': kwargs.get('source_currency', 'KRW'),
        'to': kwargs.get('target_currency', 'EUR'),
        'amount': kwargs.get('amount', 1),
        'format': 'json'
    }

    url = 'https://api.getgeoapi.com/v2/currency/convert'

    response = requests.get(url, parameters)

    amount_in_target_currency = float(
        response.json()['rates'][target_currency]['rate_for_amount'])

    return amount_in_target_currency


if __name__ == '__main__':
    # FIXME: ImportError: attempted relative import with no known parent package
    from ..config_loader.config_loader import load_config
    from pathlib import Path

    config_dir = Path(__file__).parent.parent / 'config'
    config = load_config(config_dir / 'base.json')

    rate_for_amount = check_currency_rate(**config['currency'])
    print(rate_for_amount)
