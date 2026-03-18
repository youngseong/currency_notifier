import asyncio
from datetime import datetime, timezone
from pathlib import Path

from config_loader.config_loader import load_config
from currency_checkers import init_currency_checker
from triggers.threshold_trigger import threshold_trigger
from notifiers.telegram_notifier import TelegramNotifier


_COMPARATOR_SYMBOL = {'gt': '&gt;', '>': '&gt;', 'lt': '&lt;', '<': '&lt;'}


def generate_message(src_curr: str,
                     src_amount: float,
                     results: list) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    lines = [f'<b>Rate Alert</b>  |  {timestamp}']

    for dst_curr, dst_amount, trigger in results:
        threshold = trigger['threshold']
        comparator = trigger['comparator']
        delta = dst_amount - threshold
        cmp_symbol = _COMPARATOR_SYMBOL[comparator]
        delta_sign = '+' if delta >= 0 else '-'

        lines += [
            '',
            f'<b>{src_curr} → {dst_curr}</b>',
            f'{src_amount:,} {src_curr} = <b>{dst_amount:,.2f} {dst_curr}</b>',
            f'Threshold: {cmp_symbol} {threshold:,.2f} {dst_curr}  ({delta_sign}{abs(delta):,.2f})',
        ]

    return '\n'.join(lines)


async def main():
    config_dir = Path(__file__).parent / 'config'
    config = load_config(config_dir / 'config.json')

    curr = config['currency']
    src_curr = curr['base']
    src_amount = curr['amount']

    triggered = []
    for target, trigger in curr['targets'].items():
        checker = init_currency_checker(
            api=curr['api'],
            api_key=curr['api_key'],
            base=src_curr,
            target=target,
        )
        dst_amount = checker.get_exchange_rate(amount=src_amount)
        if threshold_trigger(dst_amount, **trigger):
            triggered.append((target, dst_amount, trigger))

    if triggered:
        msg = generate_message(src_curr, src_amount, triggered)
        notifier = TelegramNotifier(**config['notification'])
        await notifier.notify_all(msg)


def lambda_handler(event, context):
    asyncio.run(main())


if __name__ == '__main__':
    asyncio.run(main())
