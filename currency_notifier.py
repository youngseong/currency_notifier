import asyncio
from datetime import datetime
from pathlib import Path

from config_loader.config_loader import load_config
from currency_checkers.geoapi import check_currency_rate
from triggers.threshold_trigger import threshold_trigger
from notifiers.telegram_notifier import TelegramNotifier


def generate_message(source_amount:float,
                     target_amount:float,
                     good:bool,
                     trigger:dict):
    lines = [
        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'Suggestion: ' + ('Exchange' if good else 'Wait'),
        f'Expected Target Amount: {target_amount}',
        f'Source Amount: {source_amount}',
        f'Trigger: {trigger}'
    ]
    return '\n'.join(lines)


async def main():
    config_dir = Path(__file__).parent / 'config'
    config = load_config(config_dir / 'base.json', config_dir / 'young.json')

    expected_amount = check_currency_rate(**config['currency'])
    good = threshold_trigger(expected_amount, **config['trigger'])

    source_amount = config['currency'].get('amount', 1)
    msg = generate_message(source_amount, expected_amount, good, config['trigger'])

    notifier = TelegramNotifier(**config['notification'])
    await notifier.notify(msg)


def lambda_handler(event, context):
    asyncio.run(main())


if __name__ == '__main__':
    asyncio.run(main())
