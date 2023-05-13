import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

FOREMAN_TOKEN = os.getenv('FOREMAN_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CONFIG_FILE = 'config.ini'
API_URL = 'https://api.foreman.mn/api/v2/clients/'
ASIC_PORT = 4028
BASE_DIR = Path(__file__).parent


def configure_logging():
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'asicscanner.log'
    rotating_handler = RotatingFileHandler(log_file, maxBytes=10 ** 6, backupCount=5)

    logging.basicConfig(
        datefmt='%Y-%m-%d_%H-%M-%S',
        format='"%(asctime)s - [%(levelname)s] - %(message)s"',
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
