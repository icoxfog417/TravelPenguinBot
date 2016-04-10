import json
import requests
from linebot.models.line_request import LineRequest
from linebot.models.line_response import LineResponse


class Line():
    HOST = "trialbot-api.line.me"

    def __init__(self,
                 channel_id,
                 channel_secret,
                 mid):
        self.channel_id = channel_id
        self.channel_secret = channel_secret
        self.mid = mid

    @classmethod
    def receive(cls, body) -> [LineRequest]:
        _b = body
        if _b is str:
            _b = json.loads(_b)

        return LineRequest.parse(_b)

    def post(self, message: LineResponse):
        url = self.__make_url("/v1/events")
        headers = {
            "Content-type": "application/json; charset=UTF-8",
            "X-Line-ChannelID": self.channel_id,
            "X-Line-ChannelSecret": self.channel_secret,
            "X-Line-Trusted-User-With-ACL": self.mid
        }

        r_dict = message.to_dict()

        resp = requests.post(url, data=r_dict, headers=headers)
        if not resp.ok:
            resp.raise_for_status()

    def __make_url(self, path):
        url = "https://" + self.HOST + path
        return url
