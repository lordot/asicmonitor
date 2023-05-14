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
        sites.append(
            Site(
                config[site].name,
                int(config[site]["chat_id"]),
                config[site]["client_id"],
                ranges
            )
        )
    return sites


async def analyze_site(site: Site):
    logging.info(f"Start scanning: {site.name}")
    scanned = await site.scan_all()
    logging.info(f"Total scanned: {len(scanned)}")
    foreman = site.scan_foreman()
    logging.info(f"Total in Foreman: {len(foreman)}")
    missed_miners = {
        ip: workername
        for ip, workername in scanned.items()
        if ip not in foreman and workername not in foreman.values()
    }
    logging.info(f"Missed: {len(missed_miners)}")
    if missed_miners:
        miners_stats = {
            "scanned": len(scanned),
            "foreman": len(foreman),
            "missed": missed_miners
        }
        await send_report(site.chat_id, miners_stats)


async def main():
    configure_logging()
    logging.info("Script started")
    for site in read_config(CONFIG_FILE):
        await analyze_site(site)
    logging.info("Script finished")


if __name__ == "__main__":
    asyncio.run(main())
