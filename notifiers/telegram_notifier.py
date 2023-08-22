import asyncio
import telegram
from typing import List


class TelegramNotifier(object):
    def __init__(self, token: str, chat_ids: List[int] = [], **kwargs):
        self._bot = telegram.Bot(token)
        self._chat_ids = chat_ids

    @property
    def chat_ids(self):
        return self._chat_ids

    async def update_chat_ids(self):
        self._chat_ids = await self.__list_chat_ids()

    async def __list_chat_ids(self):
        updates = await self._bot.get_updates()
        chat_ids = list(set(
            [u.effective_user.id for u in updates if u.effective_user]))
        return chat_ids

    async def notify_all(self, text: str):
        if not self._chat_ids:
            await self.update_chat_ids()

        await asyncio.gather(
            *[self.send_message(id, text) for id in self._chat_ids])

    async def send_message(self, chat_id: int, text: str):
        await self._bot.send_message(text=text, chat_id=chat_id)


async def main(token: str):
    notifier = TelegramNotifier(token, chat_ids=[])

    await notifier.update_chat_ids()
    print(notifier.chat_ids)

    await notifier.send_message(notifier.chat_ids[0], 'Hello world!')


if __name__ == '__main__':
    from argparse import ArgumentParser

    arg_parser = ArgumentParser()
    arg_parser.add_argument('token', type=str)

    args = arg_parser.parse_args()

    asyncio.run(main(args.token))
