class MemberIsNoneObject(Exception):
    ...

from mentord.client import *

class Member:

    """
    #### Member object contains data
    #### about the participant.

    `Use member dictionary
    to get variables. (temporarily)`
    """

    def __init__(self, member: dict) -> None:
        self.member: dict = member

        self.__check__()

    def __check__(self) -> None:
        if self.member is None:
            raise MemberIsNoneObject("The member parameter was not passed...")

    @property
    def id(self) -> int:

        """
        Params:
            `None`

        Returns:
            `int: id member`
        """

        return int(self.member["id"])

    