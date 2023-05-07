import asyncio
import re
from ipaddress import IPv4Address
from models import Asic

PORT = 4028


async def _get_workername(ip: str, command: str = '{"command": "pools"}') -> str or None:
    """
    Функция получения имени воркера по IP
    :param ip:
    :param command:
    :return:
    """
    try:
        reader, writer = await asyncio.open_connection(ip, PORT)
        writer.write(command.encode())
        await writer.drain()
        raw_data = await reader.read(4096)
        match = re.search(r'\"User\":\"(?P<name>[^\"]*)', str(raw_data))
        if match:
            workername = match.group('name')
            return workername
        return None
    except Exception as e:
        print(f"Error retrieving workername for IP {ip}: {e}")
        return


async def _check_online(ip: str) -> Asic | None:
    """
    Проверяет IP на наличие открытого порта 4028
    :param ip:
    :return: ip, online, workername
    """
    try:
        _, writer = await asyncio.wait_for(asyncio.open_connection(ip, PORT), timeout=3)
        writer.close()
        await writer.wait_closed()
        workername = await _get_workername(ip)
        if workername is None:
            return None
        asic = Asic(ip, workername)
        return asic
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None


async def scan_range(start_ip: str, end_ip: str) -> list:
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

    results = [x for x in await asyncio.gather(*tasks) if x is not None]
    return results
