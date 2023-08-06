class MessageIsNoneObject(Exception):
    ...

from .channel import *
from .guild import *
from mentord.httpc import *
from .member import *


class Message:

    """
    #### Message object contains data
    #### about a message in a certain guild and in a certain channel.
    """

    def __init__(self, message: dict) -> None:
        self.message: dict = message

    def __check__(self) -> None:
        if self.message is None:
            raise MessageIsNoneObject("The message parameter was not passed...")

    @property
    def id(self) -> int:
        """
        Params:
            `None`

        Returns:
            `int: id message`
        """

        self.__check__()

        return int(self.message["id"])

    @property
    def channel_id(self) -> int:
        """
        Params:
            `None`

        Returns:
            `int: channel id message`
        """

        self.__check__()

        return int(self.message["channel_id"])

    @property
    def content(self) -> str:
        """
        Params:
            `None`

        Returns:
            `str: content message`
        """

        self.__check__()

        return str(self.message["channel_id"])

    @property
    def author(self) -> str:
        """
        Params:
            `None`

        Returns:
            `User: author message`
        """

        self.__check__()

        return Member(self.message["author"])
