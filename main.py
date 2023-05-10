import asyncio
import configparser

from configurations import CONFIG_FILE, DEBUG
from messages import send_report
from sites import Site


def read_config(config_file: str) -> list[Site]:
    """
    Читает конфиг файл и создает объекты класса Config
    """
    sites = []
    config = configparser.ConfigParser()
    config.read(config_file)
    for site in config.sections():
        lst = config[site]['network_ranges'].split('\n')
        ranges = set(tuple(x.replace('\n', '').split('-')) for x in lst)
        sites.append(Site(
            config[site].name,
            int(config[site]['chat_id']),
            config[site]['client_id'],
            ranges
        ))
    return sites


async def main():
    if DEBUG:
        missed = {
            'scanned': 10,
            'foreman': 20,
            'missed': {
                '192.168.1.1': 'worker1',
                '192.168.1.2': 'worker2',
                '192.168.1.3': 'worker3'
            }
        }
    else:
        for site in read_config(CONFIG_FILE):
            # Получение майнеров, отсканированных в заданных диапазонах
            scanned = await site.scan_all()
            print(f"Total scanned: {len(scanned)}")

            print('Вырубай')
            await asyncio.sleep(10)
            # Получение майнеров, зарегистрированных в Foreman API
            foreman = site.scan_foreman()
            print(f"Total in Foreman: {len(foreman)}")

            # Поиск отсутствующих майнеров в Foreman
            missed = {
                'scanned': len(scanned),
                'foreman': len(foreman),
                'missed': {}
            }
            for ip, workername in scanned.items():
                if ip not in foreman and workername not in foreman.values():
                    missed.get('missed')[ip] = workername

            # Отправка отчета в телеграм
            await send_report(site.chat_id, missed)

            print('Включай!')
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
