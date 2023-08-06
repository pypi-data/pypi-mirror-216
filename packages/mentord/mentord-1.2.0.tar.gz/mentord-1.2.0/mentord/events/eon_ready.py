from threading import Thread
from time import sleep

from mentord.classes.user import User
from mentord.client import Client, IncorrectToken
from mentord.httpc import *

class on_ready:

    """
    #### The function will be called when the bot is fully ready.
    """

    def __init__(self, client: Client, rdelay: float = 5.0):
        self.client: client.Client = client
        self.rdelay: float = rdelay

    def __call__(self, func) -> None:
        while self.client.user is None:
            sleep(0.5)

        self.create_thread(self.reconnect_loop)

        func()

    def reconnect_loop(self) -> None:
        while True:
            connect_request = MentordRequest(
                url="https://discordapp.com/api/v9/users/@me",
                headers={
                    "Authorization": self.client.user.token,
                    "Content-Type": "application/json",
                },
            ).GET()

            if connect_request.status_code != 200:
                raise IncorrectToken(
                    "check a token, it is invalid."
                )
                exit()

            self.client.user: User = User(
                connect_request.json(), self.client.user.token
            )

            sleep(self.rdelay)

    def create_thread(self, func) -> None:
        new_t = Thread(target=func)
        new_t.start()
