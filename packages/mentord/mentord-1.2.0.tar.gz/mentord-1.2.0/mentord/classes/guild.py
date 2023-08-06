class GuildIsNoneObject(Exception):
    ...

from mentord.client import *

class Guild:

    """
    #### Guild object contains data
    #### about the guild.
    """

    def __init__(self, guild: dict) -> None:
        self.guild: dict = guild

        self.__check__()

    def __check__(self) -> None:
        if self.guild is None:
            raise GuildIsNoneObject("The guild parameter was not passed...")

    @property
    def id(self) -> int:
        """
        Params:
            `None`

        Returns:
            `int: id guild`
        """

        return int(self.guild["id"])

    @property
    def name(self) -> str:
        """
        Params:
            `None`

        Returns:
            `str: name guild`
        """

        return str(self.guild["name"])

    @property
    def icon(self) -> str:
        """
        Params:
            `None`

        Returns:
            `str: icon guild in hash`
        """

        return str(self.guild["icon"])

    @property
    def owner_id(self) -> int:
        """
        Params:
            `None`

        Returns:
            `int: owner guild id`
        """

        return int(self.guild["owner_guild"])
