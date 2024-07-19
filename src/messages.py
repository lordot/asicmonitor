import logging

from telegram import Bot
from telegram.constants import ParseMode

from src.configurations import TELEGRAM_TOKEN


def _create_message(miners: dict) -> str:
    message_lines = [
        *("{} {} is not in Foreman!".format(workername, ip)
          for workername, ip in miners.get('missed').items()),
        f"\nTotal IP scanned: {miners.get('scanned')}",
        f"Total in Foreman: {miners.get('foreman')}",
        f"<b>Total missed: {len(miners.get('missed'))}</b>"
    ]
    return "\n".join(message_lines)


async def send_report(chat_id, miners):
    bot = Bot(TELEGRAM_TOKEN)
    message = _create_message(miners)
    async with bot:
        await bot.send_message(chat_id, message, ParseMode.HTML)
    logging.info("The message sent to Telegram")
