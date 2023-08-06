class Member:

    """
    Класс представляющий информацию о участнике.
    """

    def __init__(self, member: dict):

        self.member: dict = member

    @property
    def id(self) -> str:

        return self.member['id']

    @property
    def username(self) -> str:

        return self.member['username']

    @property
    def global_name(self) -> str:

        return self.member['global_name']

    @property
    def avatar(self) -> str:

        return self.member['avatar']

    def get_json_object(self) -> dict:

        return self.member
