import requests


class HttpClient:

    """
    Класс для отправки запросов к API.
    """

    def __init__(self):
        ...

    def request(self, method: str, url: str, header: dict, json: dict = None) -> requests.Response:

        match method:

            case "POST":

                return self.post_request(url, header, json)

            case "GET":

                return self.get_request(url, header, json)

    def get_request(self, url: str, header: dict, json: dict = None) -> requests.Response:

        if json is not None:

            return requests.get(url=url, headers=header, json=json)

        return requests.get(url=url, headers=header)

    def post_request(self, url: str, header: dict, json: dict) -> requests.Response:

        return requests.post(url=url, headers=header, json=json)
