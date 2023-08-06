class IncorrectToken(Exception):
    ...


from .classes.user import User
from .httpc import *
from .events import *


class Client:

    """
    #### Main client class.
    """

    def __init__(self) -> None:
        self.user: User = None

    def connect(self, token: str) -> None:
        """
        Params:
            `str`: token

        Returns:
            `None`
        """

        if token is None and token.__len__() <= 0:
            raise IncorrectToken("check a token, it is invalid.")

        connect_request = MentordRequest(
            url="https://discordapp.com/api/v9/users/@me",
            headers={"Authorization": token, "Content-Type": "application/json"},
        ).GET()

        if connect_request.status_code != 200:
            raise IncorrectToken("check a token, it is invalid.")

        self.user: User = User(connect_request.json(), token)
