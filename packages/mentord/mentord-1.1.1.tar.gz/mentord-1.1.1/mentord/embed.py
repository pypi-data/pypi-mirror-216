from .eother import *


class Embed:

    def __init__(self, description: str = "", author: Author = None, fields: list[Field] = [], title: str = "", url: str = None, image: Image = None, thumbnail: Thumbnail = None, footer: Footer = None, timestamp: str = ""):

        self.description: str = description
        self.author: Author = author
        self.fields: list[Field] = fields
        self.title: str = title
        self.url: str = url
        self.image: Image = image
        self.footer: Footer = footer
        self.thumbnail: Thumbnail = thumbnail
        self.timestamp: str = timestamp

    def get_json(self) -> dict:

        return {
            "description": self.description,
            "fields": [field for field in self.fields],
            "author": self.get_author(),
            "title": self.title,
            "url": self.url,
            "image": self.get_image(),
            "thumbnail": self.get_thumbnail(),
            "timestamp": self.timestamp
        }

    def get_author(self) -> dict:

        if self.author is None:

            return {}

        return self.author.get_json()

    def get_image(self) -> dict:

        if self.image is None:

            return {}

        return self.image.get_json()

    def get_thumbnail(self) -> dict:

        if self.thumbnail is None:

            return {}

        return self.thumbnail.get_json()
