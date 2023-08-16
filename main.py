from config_loader.config_loader import load_config
from currency_checkers.geoapi import check_currency_rate
from triggers.threshold_trigger import threshold_trigger
from pathlib import Path


def main():
    config_dir = Path(__file__).parent / 'config'
    config = load_config(config_dir / 'base.json', config_dir / 'young.json')

    expected_amount = check_currency_rate(**config['currency'])
    good = threshold_trigger(expected_amount, **config['trigger'])

    # TODO: alert currency rate and suggestion (i.e., exchange or not) to the user


if __name__ == '__main__':
    main()
