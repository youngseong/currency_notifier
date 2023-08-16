import asyncio
from datetime import datetime
from pathlib import Path

from config_loader.config_loader import load_config
from currency_checkers.geoapi import check_currency_rate
from triggers.threshold_trigger import threshold_trigger
from notifiers.telegram_notifier import TelegramNotifier


def generate_message(amount:float, good:bool, trigger:dict):
    lines = [
        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        f'Suggestion: {str(good)}',
        f'Expected Target Amount: {amount}',
        f'Trigger: {trigger}'
    ]
    return '\n'.join(lines)


async def main():
    config_dir = Path(__file__).parent / 'config'
    config = load_config(config_dir / 'base.json', config_dir / 'young.json')

    expected_amount = check_currency_rate(**config['currency'])
    good = threshold_trigger(expected_amount, **config['trigger'])

    msg = generate_message(expected_amount, good, config['trigger'])

    notifier = TelegramNotifier(**config['notification'])
    await notifier.notify(msg)


if __name__ == '__main__':
    asyncio.run(main())
