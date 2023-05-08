from os import getenv

from dotenv import load_dotenv

load_dotenv()

DEBUG = False
CLIENT_ID = getenv('CLIENT_ID')
FOREMAN_TOKEN = getenv('FOREMAN_TOKEN')
TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
CHAT_ID = getenv('CHAT_ID')


def get_addresses() -> set[tuple[str, ...]]:
    """
    Функция считывает адреса из файла config.ini
    :return:
    """
    with open('config.ini', 'r') as file:
        return set(
            tuple(x.replace('\n', '').split('-')) for x in file.readlines()
        )
