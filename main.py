import asyncio

from configurations import get_addresses

from foreman import get_foreman_api_miners
from models import Asic
from scanner import scan_range
from configurations import DEBUG


if __name__ == "__main__":
    scanned_miners = []
    for ips in get_addresses():
        loop = asyncio.get_event_loop()
        scanned_miners.extend(loop.run_until_complete(scan_range(ips[0], ips[1])))
    print(f'Total scanned: {len(scanned_miners)}')

    foreman_miners = get_foreman_api_miners()
    print(f"Total in Foreman: {foreman_miners.get('total')}")

    if DEBUG:
        asic = Asic('1.1.1.1', 'test.workername')
        scanned_miners.append(asic)

    for asic in scanned_miners:
        if asic.ip not in foreman_miners.get('miners'):
            if asic.workername not in foreman_miners.get('miners').values():
                print(f'{asic.workername} {asic.ip} not in Foreman!')
