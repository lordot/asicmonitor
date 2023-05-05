import asyncio
import re
import ipaddress

PORT = 4028


async def get_workername(ip: str, command: str = '{"command": "pools"}') -> str or None:
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


async def check_online(ip: str) -> tuple[str, bool, str | None]:
    """
    Проверяет IP на наличие открытого порта 4028
    :param ip:
    :return: ip, online, workername
    """
    try:
        _, writer = await asyncio.wait_for(asyncio.open_connection(ip, PORT), timeout=3)
        writer.close()
        await writer.wait_closed()
        workername = await get_workername(ip)
        return ip, True, workername
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return ip, False, None


async def scan_network(start_ip: str, end_ip: str) -> None:
    """
    Сканирует диапазон сети и возвращает все майнеры онлайн с именами
    :param start_ip:
    :param end_ip:
    :return:
    """
    start_ip = ipaddress.IPv4Address(start_ip)
    end_ip = ipaddress.IPv4Address(end_ip)

    tasks = []
    for ip_int in range(int(start_ip), int(end_ip) + 1):
        ip = str(ipaddress.IPv4Address(ip_int))
        tasks.append(asyncio.ensure_future(check_online(ip)))

    results = [x for x in await asyncio.gather(*tasks) if x[1]]

    for res in results:
        print(f"{res[0]} is online. Workername: {res[2]}")

    print(f'Total: {len(results)}')

if __name__ == "__main__":
    start_ip = "10.6.71.1"
    end_ip = "10.6.71.254"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scan_network(start_ip, end_ip))
