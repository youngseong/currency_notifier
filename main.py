from config_loader.config_loader import load_config
from currency_checkers.geoapi import check_currency_rate
from pathlib import Path


def main():
    config_dir = Path(__file__).parent / 'config'
    config = load_config(config_dir / 'base.json', config_dir / 'young.json')

    currency_rate_for_amount = check_currency_rate(**config)

    # TODO's
    # 2. check if the rate triggers a condition
    # 3. if so, alert to the user


if __name__ == '__main__':
    main()
