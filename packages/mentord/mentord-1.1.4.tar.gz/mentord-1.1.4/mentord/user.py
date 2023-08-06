from .channel import *
from .guild import *
from .http_ import *
from .message import *


class User:

    """
    Класс представляющий информацию о текущем подключенном объекте.
    """

    def __init__(self, user: dict, token: str):

        self.user: dict = user
        self.token: str = token

    @property
    def id(self) -> str:

        return self.user['id']

    @property
    def username(self) -> str:

        return self.user['username']

    @property
    def global_name(self) -> str:

        return self.user['global_name']

    @property
    def avatar(self) -> str:

        return self.user['avatar']

    @property
    def banner_color(self) -> str:

        return self.user['banner_color']


    def get_json_object(self) -> dict:

        return self.user

    @property
    def channels(self) -> list[Channel]:

        user_channels: list[Channel] = []

        for channel in HttpClient().request("GET", 'https://discordapp.com/api/v9/users/@me/channels',
                                            {"Authorization": self.token, "Content-Type": "application/json"}).json():

            user_channels.append(Channel(channel, self.token))

        return user_channels

    @property
    def guilds(self) -> list[Guild]:

        user_guilds: list[Guild] = []

        for guild in HttpClient().request("GET", 'https://discordapp.com/api/v9/users/@me/guilds',
                                          {"Authorization": self.token, "Content-Type": "application/json"}).json():

            user_guilds.append(Guild(guild, self.token))

        return user_guilds
