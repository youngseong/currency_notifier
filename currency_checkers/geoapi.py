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
    from argparse import ArgumentParser

    arg_parser = ArgumentParser()
    arg_parser.add_argument('api_key', type=str)

    args = arg_parser.parse_args()

    rate_for_amount = check_currency_rate(args.api_key)
    print(rate_for_amount)
