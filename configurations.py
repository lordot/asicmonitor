import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = False
FOREMAN_TOKEN = os.getenv('FOREMAN_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CONFIG_FILE = 'config.ini'
API_URL = 'https://api.foreman.mn/api/v2/clients/'
ASIC_PORT = 4028
