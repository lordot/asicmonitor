from os import getenv
from dotenv import load_dotenv

load_dotenv()

DEBUG = getenv('DEBUG')
CLIENT_ID = getenv('CLIENT_ID')
TOKEN = getenv('TOKEN')


def get_addresses():
    """
    Функция считывает адреса из файла config.ini
    :return:
    """
    with open('config.ini', 'r') as file:
        return [x.replace('\n', '').split('-') for x in file.readlines()]
