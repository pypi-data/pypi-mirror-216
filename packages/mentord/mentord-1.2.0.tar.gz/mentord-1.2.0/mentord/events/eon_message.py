from threading import Thread
from time import sleep

from mentord.classes.message import Message
from mentord.client import *
from mentord.httpc import *
from requests import Response


class on_message:

    """
    #### The function will be called when a new message is received.
    """

    def __init__(self, client: Client, delay: float = 0.5):
        self.client: Client = client
        self.delay: float = delay

    def __call__(self, *func) -> None:
        while self.client.user is None:
            sleep(0.5)

        self.create_thread(func=self.update_loop, args=func)

    def get_messages_id(self) -> dict:
        messages: dict = {}

        for channel in self.client.user.get_channels():
            messages[channel.id] = channel.messages(token=self.client.user.token)[0].id

        return messages

    def get_request(self, channel_id: int, message_id: int) -> Response:
        return MentordRequest(
            url="https://discordapp.com/api/v9/channels/{0}/messages?after={1}&limit=1".format(
                channel_id, message_id
            ),
            headers={
                "Authorization": self.client.user.token,
                "Content-Type": "application/json",
            },
        ).GET()

    def update_loop(self, func) -> None:
        messages: dict = self.get_messages_id()

        while True:
            for channel in self.client.user.get_channels():
                try:
                    response = self.get_request(channel.id, messages[channel.id])
                except:
                    messages: dict = self.get_messages_id()

                if response.json().count != 0:
                    for message in response.json():
                        func(Message(message))
                        messages[channel.id] = Message(message).id

            sleep(self.delay)

    def create_thread(self, func, args) -> None:
        new_t = Thread(target=func, args=args)
        new_t.start()
