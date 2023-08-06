from .member import *

class Message:

    def __init__(self, message: dict):

        self.message: dict = message
    
    def get_json_object(self) -> dict:

        return self.message
    
    @property
    def id(self) -> str:

        return str(self.message['id'])
    
    @property
    def channel_id(self) -> str:

        return str(self.message['channel_id'])
    
    @property
    def author(self) -> Member:

        return Member(self.message['author'])

    @property
    def content(self) -> str:

        return str(self.message['content'])