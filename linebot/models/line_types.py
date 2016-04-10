from enum import Enum


class EventType(Enum):
    message = "138311609000106303"
    operation = "138311609100106403"


class ContentType(Enum):
    text = 1
    image = 2
    video = 3
    audio = 4
    location = 7
    sticker = 8
    contact = 10
