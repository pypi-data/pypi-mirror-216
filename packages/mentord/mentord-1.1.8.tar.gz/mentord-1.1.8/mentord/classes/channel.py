class ChannelIsNoneObject(Exception):
    ...


from .message import *
from .guild import *
from httpc import *


class Channel:

    """
    #### Channel object contains data
    #### about the channel in guild.
    """

    def __init__(self, channel: dict) -> None:
        self.channel: dict = channel

    def __check__(self) -> None:
        if self.channel is None:
            raise ChannelIsNoneObject("The Channel parameter was not passed...")

    @property
    def id(self) -> int:
        """
        Params:
            `None`

        Returns:
            `int: id channel`
        """

        self.__check__()

        return int(self.channel["id"])

    @property
    def last_message_id(self) -> int:
        """
        Params:
            `None`

        Returns:
            `int: last message id`
        """

        self.__check__()

        return int(self.channel["last_message_id"])

    @property
    def recipients(self) -> int:
        """
        Params:
            `None`

        Returns:
            `dict: recipients`

        Keys:
            `id: int (id member)`
            `username: str (username member)`
            `global_name: str (global_name member)`
            `avatar: str (avatar user hash)`
        """

        self.__check__()

        return dict(self.channel["recipients"])

    def messages(self, token: str) -> list[Message]:
        """
        Params:
            `None`

        Returns:
            `list[Message]: list messages object in current channel`
        """

        self.__check__()

        response = MentordRequest(
            url="https://discordapp.com/api/v9/channels/{0}/messages?limit=25".format(
                self.id
            ),
            headers={
                "Authorization": token,
                "Content-Type": "application/json",
            },
        ).GET()

        return list[Message](Message(message) for message in response.json())
