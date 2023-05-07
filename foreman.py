from requests import request
from configurations import CLIENT_ID, TOKEN

URL = f'https://api.foreman.mn/api/v2/clients/{CLIENT_ID}'


def _get_total_miners() -> int:
    """
    Находит общее количество майнеров по Client_ID
    :return: общее количество майнеров
    """
    response = request('get', URL, headers={'Authorization': 'Token ' + TOKEN}).json()
    try:
        return response[0]['miners']['total']
    except KeyError:
        if len(response) < 2:
            raise Exception(response.get('detail'))
        raise KeyError(f"Can't find total miners key in API {URL}")


def get_foreman_api_miners() -> dict:
    """
    Собирает все майнеры
    :return: словарь с майнерами {ip: workername}
    """
    total = _get_total_miners()
    offset = 0
    result = {'total': total, 'miners': {}}
    while offset < total:
        url = URL + f'/miners?limit=500&offset={offset}'
        response = request('get', url, headers={'Authorization': 'Token ' + TOKEN})
        for miner in response.json()["results"]:
            ip = miner.get('ip')
            pools = miner.get("pools", [])
            if pools:
                worker = pools[0].get("worker", None)
            else:
                worker = None
            result['miners'][ip] = worker
        offset += 500
    return result
