from .embed import *
from .http_ import *
from .member import *
from .message import *


class Channel:

    """
    Класс представляющий информацию о канале.
    """

    def __init__(self, channel: dict, token: str):

        self.channel: dict = channel
        self.token: str = token

    @property
    def id(self) -> str:

        """
        Id канала.
        """

        return str(self.channel['id'])

    @property
    def member(self) -> Member:

        """
        Соучастник канала.
        """

        return Member(self.channel['recipients'][0])
    
    @property
    def messages(self) -> list[Message]:
        
        """
        Получение некоторых сообщений из канала.
        """

        user_messages: list[Message] = []

        for message in HttpClient().request("GET", 'https://discordapp.com/api/v9/channels/{0}/messages'.format(self.id),
                                            {"Authorization": self.token, "Content-Type": "application/json"}).json():

            user_messages.append(Message(message))

        return user_messages


    def get_json_object(self) -> dict:

        """
        Получить объект в виде словаря.
        """

        return self.channel
    
    def send_message(self, content: str = "", embeds: list[Embed] = []) -> any:

        """
        Отправить сообщение в данный канал.
        """

        repsonse = HttpClient().request("POST", 'https://discordapp.com/api/v9//channels/{0}/messages'.format(self.id),
                            header={"Authorization": self.token, "Content-Type": "application/json"}, json={
                                'content': content,
                                'tts': False,
                                'embeds': embeds
                                })
        
        if repsonse.status_code != 200:

            return False
        
        return True
