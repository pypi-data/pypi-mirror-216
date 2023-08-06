from http_ import *
from member import *


class Guild:

    """
    Класс представляющий информацию о гильдии.
    """

    def __init__(self, guild: dict, token: str):

        self.guild: dict = guild
        self.token: str = token

    @property
    def id(self) -> str:

        return self.guild['id']

    @property
    def name(self) -> str:

        return self.guild['name']

    @property
    def is_owner(self) -> bool:

        return self.guild['owner']

    def get_json_object(self) -> dict:

        return self.guild

    @property
    def members(self) -> list[Member]:

        guild_members: list[Member] = []

        for guild in HttpClient().request("GET", 'https://discordapp.com/api/v9/guilds/{0}/members'.format(self.id),
                                          {"Authorization": self.token, "Content-Type": "application/json"}).json():

            guild_members.append(Member(guild))

        return guild_members

    @property
    def members_count(self) -> int:

        return self.members.count
