from classes import Channel
from client import Client
from httpc import *


class ChannelOperations:

    """
    #### Channel operations...
    """

    def __init__(self, channel: Channel, client: Client):
        self.channel: Channel = channel
        self.client: Client = client

    def send_message(self, content: str) -> None:
        response = MentordRequest(
            url="https://discordapp.com/api/v9/channels/{0}/messages".format(
                self.channel.id
            ),
            headers={
                "Authorization": self.client.user.token,
                "Content-Type": "application/json",
            },
        ).POST(json={"content": content})

        if response.status_code != 200:
            raise Exception("Error request send...")
