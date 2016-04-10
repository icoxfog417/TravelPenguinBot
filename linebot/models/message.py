from collections import namedtuple
from linebot.models.line_types import ContentType
from linebot.models.line_response import LineResponse


Location = namedtuple("Location", ["title", "address", "latitude", "longitude"])


class Message():

    def __init__(self,
                 message_id="",
                 content_type=ContentType.text,
                 from_mid="",
                 created_time=0,
                 to_mids=(),
                 to_type=1,
                 content_metadata=None,
                 text="",
                 location=None):
        self.message_id = message_id
        self.content_type = content_type
        self.from_mid = from_mid
        self.created_time = created_time  # todo: to datetime
        self.to_mids = list(to_mids)
        self.to_type = to_type
        self.content_metadata = content_metadata
        self.text = text
        self.location = location

    @classmethod
    def parse(cls, body):
        instance = Message(
            body["id"],
            ContentType(int(body["contentType"])),
            body["from"],
            body["createdTime"],
            body["to"],
            body["toType"],
            body["contentMetadata"],
            body["text"]
        )

        if "location" in body and body["location"] is not None:
            loc = body["location"]
            instance.location = Location(loc["title"], loc["address"], loc["latitude"], loc["longitude"])

        return instance

    def reply(self) -> LineResponse:
        resp = LineResponse(self.from_mid)
        return resp
