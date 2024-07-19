import asyncio
import re
from ipaddress import IPv4Address

from src.configurations import ASIC_PORT


class ScannerMixin:
    def __init__(self, ranges: set):
        self.ranges = ranges

    async def _get_workername(self, ip: str) -> str:
        """
        Функция получения имени воркера по IP
        :param ip:
        :param command:
        :return:
        """
        command = '{"command": "pools"}'
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, ASIC_PORT), timeout=10
            )
            writer.write(command.encode())
            await writer.drain()
            raw_data = await asyncio.wait_for(reader.read(4096), timeout=3)
            match = re.search(r'\"User\":\"(?P<name>[^\"]*)', str(raw_data))
            if match:
                return match.group('name')
            return 'Unknown'
        except (asyncio.TimeoutError, Exception):
            return 'Unknown'

    async def _check_online(self, ip: str) -> bool:
        """
        Проверяет IP на наличие открытого порта 4028
        :param ip:
        :return: True если порт открыт, иначе False
        """
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, ASIC_PORT), timeout=3
            )
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return False

    async def _scan_range(self, start_ip: str, end_ip: str) -> dict:
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
            tasks.append(asyncio.ensure_future(self._check_online(ip)))

        online = [ip for ip, online in zip(
            range(int(start_ip), int(end_ip) + 1
                  ), await asyncio.gather(*tasks)) if online]

        workername_tasks = [asyncio.ensure_future(
            self._get_workername(str(IPv4Address(ip)))
        ) for ip in online]
        worker_names = await asyncio.gather(*workername_tasks)

        return {str(IPv4Address(k)): v for k, v in zip(online, worker_names)}

    async def scan_all(self) -> dict:
        """
        Сканирует сет всех диапозонов адресов
        :param address:
        :return: словарь с майнерами {ip: workername}
        """
        scanned = {}
        for ips in self.ranges:
            scanned.update(await self._scan_range(ips[0], ips[1]))
        return scanned
