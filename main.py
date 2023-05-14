import asyncio
import configparser
import logging
import os

from configurations import CONFIG_FILE, configure_logging
from messages import send_report
from sites import Site


def read_config(config_file: str) -> list[Site]:
    """
    Читает конфиг файл и создает объекты класса Config
    """
    file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        config_file
    )
    sites = []
    config = configparser.ConfigParser()
    config.read(file)
    for site in config.sections():
        lst = config[site]["network_ranges"].split("\n")
        ranges = set(tuple(x.replace("\n", "").split("-")) for x in lst)
        sites.append(Site(
            config[site].name,
            int(config[site]["chat_id"]),
            config[site]["client_id"],
            ranges
        ))
    return sites


async def main():
    configure_logging()
    logging.info("Script started")
    # Перебираем все конфигурации из файла CONFIG_FILE
    for site in read_config(CONFIG_FILE):
        logging.info(f"Start scanning: {site.name}")
        # Получение майнеров, отсканированных в заданных диапазонах
        scanned = await site.scan_all()
        logging.info(f"Total scanned: {len(scanned)}")

        # Получение майнеров, зарегистрированных в Foreman API
        foreman = site.scan_foreman()
        logging.info(f"Total in Foreman: {len(foreman)}")

        # Поиск отсутствующих майнеров в Foreman
        miners = {
            "scanned": len(scanned),
            "foreman": len(foreman),
            "missed": {}
        }
        for ip, workername in scanned.items():
            if ip not in foreman and workername not in foreman.values():
                miners.get("missed")[ip] = workername
        logging.info(f"Missed: {len(miners.get('missed'))}")

        if len(miners.get("missed")) > 0:
            # Отправка отчета в телеграм
            await send_report(site.chat_id, miners)

    logging.info("Script finished")

if __name__ == "__main__":
    asyncio.run(main())
