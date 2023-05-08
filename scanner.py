import asyncio
import re
from ipaddress import IPv4Address

PORT = 4028


async def _get_workername(ip: str) -> str:
    """
    Функция получения имени воркера по IP
    :param ip:
    :param command:
    :return:
    """
    command = '{"command": "pools"}'
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, PORT), timeout=10
        )
        writer.write(command.encode())
        await writer.drain()
        raw_data = await asyncio.wait_for(reader.read(4096), timeout=10)
        match = re.search(r'\"User\":\"(?P<name>[^\"]*)', str(raw_data))
        if match:
            return match.group('name')
        return 'Unknown'
    except (asyncio.TimeoutError, Exception):
        return 'Unknown'


async def _check_online(ip: str) -> bool:
    """
    Проверяет IP на наличие открытого порта 4028
    :param ip:
    :return: True если порт открыт, иначе False
    """
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, PORT), timeout=3
        )
        writer.close()
        await writer.wait_closed()
        return True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return False


async def scan_range(start_ip: str, end_ip: str) -> dict:
    """
    Сканирует диапазон сети и возвращает все майнеры онлайн с именами
    :param start_ip:
    :param end_ip:
    :return:
    """
    start_ip = IPv4Address(start_ip)
    end_ip = IPv4Address(end_ip)

    tasks = []
    for ip_int in range(int(start_ip), int(end_ip) + 1):
        ip = str(IPv4Address(ip_int))
        tasks.append(asyncio.ensure_future(_check_online(ip)))

    online_ips = [ip for ip, online in zip(
        range(int(start_ip), int(end_ip) + 1
              ), await asyncio.gather(*tasks)) if online]

    workername_tasks = [asyncio.ensure_future(
        _get_workername(str(IPv4Address(ip)))
    ) for ip in online_ips]
    worker_names = await asyncio.gather(*workername_tasks)

    return {str(IPv4Address(k)): v for k, v in zip(online_ips, worker_names)}


def scan_all_ranges(address: set) -> dict:
    """
    Сканирует сет всех диапозонов адресов
    :param address:
    :return: словарь с майнерами {ip: workername}
    """
    scanned = {}
    for ips in address:
        loop = asyncio.get_event_loop()
        scanned.update(loop.run_until_complete(scan_range(ips[0], ips[1])))
    return scanned


if __name__ == '__main__':
    dct = scan_all_ranges({('10.6.61.10', '10.6.61.15')})
    print(dct)
