import time
from threading import Thread

from .embed import *
from .http_ import *
from .message import *
from .user import *


class Client:

    """
    Класс выполняющий подключение с API.
    """

    def __init__(self):

        self.user: User = None

    def connect(self, token: str) -> any:

        response = HttpClient().request('GET', 'https://discordapp.com/api/v9/users/@me',
                                        {"Authorization": token, "Content-Type": "application/json"})

        if response.status_code != 200:

            raise ConnectionError

        self.user = User(response.json(), token)

    @property
    def is_ready(self) -> bool:

        return self.user is not None

    def on_ready(self, func):

        while self.is_ready is False:

            time.sleep(0.5)

        func()
        new_t = Thread(target=self.connect_stable)
        new_t.start()

    def get_messages_id(self) -> dict:

        messages: dict = {}

        for channel in self.user.channels:
            
            messages[channel.id] = channel.messages[0].id
        
        return messages

    def message_processing(self, func):

        messages: dict = self.get_messages_id()

        while True:

            for channel in self.user.channels:

                response = requests.get('https://discordapp.com/api/v9/channels/{0}/messages?after={1}&limit=1'.format(channel.id, messages[channel.id]),
                                        headers={"Authorization": self.user.token, "Content-Type": "application/json"}, )

                if response.json().count != 0:

                    for message in response.json():

                        func(Message(message))
                
                        messages[channel.id] = Message(message).id

            time.sleep(1)

    def send_message(self, content: str = "", embeds: list[Embed] = [], channel_id: str = "") -> any:

        repsonse = HttpClient().request("POST", 'https://discordapp.com/api/v9//channels/{0}/messages'.format(channel_id),
                                        header={"Authorization": self.user.token, "Content-Type": "application/json"}, json={
            'content': content,
            'tts': False,
            'embeds': embeds
        })

        if repsonse.status_code != 200:

            return False

        return True

    def connect_stable(self):

        while True:

            self.connect(self.user.token)
            time.sleep(5)

    def on_message(self, *func):

        while self.is_ready is False:

            time.sleep(0.5)

        new_t = Thread(target=self.message_processing, args=func)
        new_t.start()


class ConnectionError(Exception):

    ...


if __name__ == '__main__':

    ...
