import json
from time import sleep

from requests import request

from configurations import API_URL, FOREMAN_TOKEN

NUM_TRIES = 5
API_TIMEOUT = 1


class ForemanMixin:
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.url = API_URL + self.client_id
        self.headers = {"Authorization": "Token " + FOREMAN_TOKEN}

    def _get_json_response(self, url: str, headers) -> json:
        """
        Tries to get json response for a given number of attempts.
        """
        for _ in range(NUM_TRIES):
            response = request("get", url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                sleep(5)

        raise Exception(f"No API response: {url}. Tried {NUM_TRIES} times")

    def scan_foreman(self) -> dict:
        """
        Collects all miners.
        """
        results = {}
        offset = 0

        while True:
            url_offset_limit = self.url + f"/miners?limit=500&offset={offset}"
            response = self._get_json_response(url_offset_limit, self.headers)

            if response is None or not response.get('results'):
                break

            for miner in response["results"]:
                ip = miner.get("ip")
                pools = miner.get("pools")
                worker = pools[0].get("worker", None) if pools else None
                results[ip] = worker

            sleep(API_TIMEOUT)
            offset += 500

        return results
