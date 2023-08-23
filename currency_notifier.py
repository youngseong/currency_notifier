import asyncio
from datetime import datetime
from pathlib import Path

from config_loader.config_loader import load_config
from currency_checkers.geo_currency_checker import GeoCurrencyChecker
from triggers.threshold_trigger import threshold_trigger
from notifiers.telegram_notifier import TelegramNotifier


def generate_message(dst_amount: float,
                     good: bool,
                     currency_setting: dict,
                     trigger_setting: dict):
    src_curr = currency_setting['base']
    dst_curr = currency_setting['currency']
    src_amount = currency_setting['amount']
    lines = [
        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'Suggestion: ' + ('Exchange' if good else 'Wait'),
        f'From ({src_curr}): {src_amount}',
        f'To ({dst_curr}): {dst_amount}',
        f'Trigger: {trigger_setting}'
    ]
    return '\n'.join(lines)


async def main():
    config_dir = Path(__file__).parent / 'config'
    config = load_config(config_dir / 'config.json')

    currency_checker = GeoCurrencyChecker(**config['currency'])
    expected_amount = currency_checker.get_exchange_rate() * config['currency']['amount']

    good = threshold_trigger(expected_amount, **config['trigger'])

    msg = generate_message(expected_amount,
                           good,
                           config['currency'],
                           config['trigger'])

    notifier = TelegramNotifier(**config['notification'])
    await notifier.notify_all(msg)


def lambda_handler(event, context):
    asyncio.run(main())


if __name__ == '__main__':
    asyncio.run(main())
