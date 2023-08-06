class MemberIsNoneObject(Exception):
    ...

from mentord.client import *

class Member:

    """
    #### Member object contains data
    #### about the participant.
    """

    def __init__(self, member: dict) -> None:
        self.member: dict = member

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

        self.__check__()

        return int(self.member["id"])
