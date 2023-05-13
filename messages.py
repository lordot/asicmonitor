import logging

from telegram import Bot
from telegram.constants import ParseMode

from configurations import TELEGRAM_TOKEN


def _create_message(missed: dict) -> str:
    message_lines = [
        f"Total scanned: {missed.get('scanned')}",
        f"Total in Foreman: {missed.get('foreman')}\n"
    ]
    for workername, ip in missed.get('missed').items():
        message_lines.append(f"{workername} {ip} is not in Foreman!")

    message_lines.append(f"\n<b>Total missed: {len(missed.get('missed'))}</b>")
    return "\n".join(message_lines)


async def send_report(chat_id, missed):
    bot = Bot(TELEGRAM_TOKEN)
    message = _create_message(missed)
    async with bot:
        await bot.send_message(chat_id, message, ParseMode.HTML)
    logging.info("The message sent to telegram")
