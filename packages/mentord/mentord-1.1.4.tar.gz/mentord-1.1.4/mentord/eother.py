class Field:

    def __init__(self, name: str, value: str, inline: bool = False):

        self.name: str = name
        self.value: str = value
        self.inline: False = inline

    def get_json(self) -> dict:

        return {
            "name": self.name,
            "value": self.value,
            "inline": self.inline
        }


class Author:

    def __init__(self, name: str, url: str = None, icon_url: str = None):

        self.name: str = name
        self.url: str = url
        self.icon_url: str = icon_url

    def get_json(self) -> dict:

        return {
            "name": self.name,
            "url": self.url,
            "icon_url": self.icon_url
        }


class Image:

    def __init__(self, url: str):

        self.url: str = url

    def get_json(self) -> dict:

        return {
            "url": self.url
        }


class Thumbnail:

    def __init__(self, url: str):

        self.url: str = url

    def get_json(self) -> dict:

        return {
            "url": self.url
        }


class Footer:

    def __init__(self, text: str, icon_url: str):

        self.text: str = text
        self.icon_url: str = icon_url

    def get_json(self) -> dict:

        return {
            "text": self.text,
            "icon_url": self.icon_url
        }
