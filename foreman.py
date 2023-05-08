import json
from time import sleep

from requests import request

from configurations import CLIENT_ID, FOREMAN_TOKEN

URL = f'https://api.foreman.mn/api/v2/clients/{CLIENT_ID}'


def _get_json_response(url: str, headers) -> json:
    tries = 5
    while tries != 0:
        try:
            response = request('get', url, headers=headers).json()
            return response
        except json.decoder.JSONDecodeError:
            sleep(5)
    raise Exception(f'No API response: {url}. Tried 5 times')


def _get_total_miners() -> int:
    """
    Находит общее количество майнеров по Client_ID
    :return: общее количество майнеров
    """
    response = _get_json_response(
        URL, {'Authorization': 'Token ' + FOREMAN_TOKEN}
    )
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
    result = {}
    while offset < total:
        url = URL + f'/miners?limit=500&offset={offset}'
        response = _get_json_response(
            url, {'Authorization': 'Token ' + FOREMAN_TOKEN}
        )
        for miner in response["results"]:
            ip = miner.get('ip')
            pools = miner.get("pools", [])
            if pools:
                worker = pools[0].get("worker", None)
            else:
                worker = None
            result[ip] = worker
        offset += 500
    return result
