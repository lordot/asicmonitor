import asyncio
from time import sleep

from configurations import CHAT_ID, DEBUG, get_addresses
from foreman import get_foreman_api_miners
from messages import send_report
from scanner import scan_all_ranges


def main():
    if DEBUG:
        missed = {
            'scanned': 10,
            'foreman': 20,
            'miners': {
                '192.168.1.1': 'worker1',
                '192.168.1.2': 'worker2',
                '192.168.1.3': 'worker3'
            }
        }
    else:
        # Получение майнеров, отсканированных в заданных диапазонах
        scanned = scan_all_ranges(get_addresses())
        print(f"Total scanned: {len(scanned)}")

        # Получение майнеров, зарегистрированных в Foreman API
        foreman = get_foreman_api_miners()
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
    asyncio.run(send_report(CHAT_ID, missed))


if __name__ == "__main__":
    main()
