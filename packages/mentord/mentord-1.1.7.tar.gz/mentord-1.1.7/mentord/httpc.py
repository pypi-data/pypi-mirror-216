class RequestError(Exception):
    ...


import requests


class MentordRequest:

    """
    #### The class responsible for sending
    #### requests to the discord API.
    """

    def __init__(self, url: str, headers: dict) -> None:
        self.url: str = url
        self.headers: dict = headers

    def GET(self) -> requests.Response:
        """
        Params:
            `None`

        Returns:
            `requests.Response: output request`
        """

        return requests.get(url=self.url, headers=self.headers)

    def POST(self, json: dict = None) -> requests.Response:
        """
        Params:
            `dict: json data (Optional, default is None)`

        Returns:
            `requests.Response: output request`
        """

        if json is None:
            return requests.post(url=self.url, headers=self.headers)

        return requests.post(url=self.url, headers=self.headers, json=json)
