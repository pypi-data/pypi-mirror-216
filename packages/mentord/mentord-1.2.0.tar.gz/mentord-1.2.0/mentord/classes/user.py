class UserIsNoneObject(Exception):
    ...


from .channel import *
from .guild import *
from mentord.httpc import *


class User:

    """
    #### The User object contains data
    #### about the connected object by token.
    """

    def __init__(self, user: dict, token: str) -> None:
        self.user: dict = user
        self.token: str = token

        self.__check__()

    def __check__(self) -> None:
        if self.user is None:
            raise UserIsNoneObject("The user parameter was not passed...")

    @property
    def id(self) -> int:
        """
        Params:
            `None`

        Returns:
            `int: id user`
        """

        return int(self.user["id"])

    @property
    def username(self) -> str:
        """
        Params:
            `None`

        Returns:
            `str: username`
        """

        return str(self.user["username"])

    @property
    def global_name(self) -> str:
        """
        Params:
            `None`

        Returns:
            `str: global name`
        """

        return str(self.user["global_name"])

    @property
    def avatar(self) -> str:
        """
        Params:
            `None`

        Returns:
            `str: string hash`
        """

        return str(self.user["avatar"])

    def get_guilds(self) -> list[Guild]:
        """
        Params:
            `None`

        Returns:
            `list[Guild]: list guilds current user`
        """

        connect_request = MentordRequest(
            url="https://discordapp.com/api/v9/users/@me/guilds",
            headers={"Authorization": self.token, "Content-Type": "application/json"},
        ).GET()

        if connect_request.status_code != 200:
            raise RequestError(
                "Error request, status code: {0}".format(connect_request.status_code)
            )

        return list[Guild](Guild(guild) for guild in connect_request.json())

    def get_channels(self) -> list[Channel]:
        """
        Params:
            `None`

        Returns:
            `list[Channel]: list channels current user`
        """

        connect_request = MentordRequest(
            url="https://discordapp.com/api/v9/users/@me/channels",
            headers={"Authorization": self.token, "Content-Type": "application/json"},
        ).GET()

        if connect_request.status_code != 200:
            raise RequestError(
                "Error request, status code: {0}".format(connect_request.status_code)
            )

        return list[Channel](Channel(channel) for channel in connect_request.json())
