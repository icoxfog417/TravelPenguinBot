import json
import requests
from linebot.models.line_request import LineRequest
from linebot.models.line_response import LineResponse


class Line():
    HOST = "trialbot-api.line.me"

    def __init__(self,
                 channel_id,
                 channel_secret,
                 mid,
                 proxy=""):
        self.channel_id = channel_id
        self.channel_secret = channel_secret
        self.mid = mid
        self.proxies = {}
        if proxy:
            self.proxies = {
                "http": proxy,
                "https": proxy
            }


    @classmethod
    def receive(cls, body) -> [LineRequest]:
        _b = body
        if _b is str:
            _b = json.loads(_b)

        return LineRequest.parse(_b)

    def post(self, message: LineResponse):
        url = self.__make_url("/v1/events")
        headers = {
            "X-Line-ChannelID": self.channel_id,
            "X-Line-ChannelSecret": self.channel_secret,
            "X-Line-Trusted-User-With-ACL": self.mid,
            "Content-Type": "application/json; charset=UTF-8"
        }

        r_dict = message.to_dict()

        resp = requests.post(url, data=json.dumps(r_dict), headers=headers, proxies=self.proxies)
        if not resp.ok:
            raise Exception("Url({0}), Status({1} {2}): header={3}, proxy={4}, body={5}".format(
                url, resp.status_code, resp.reason, headers, self.proxies, r_dict
            ))

    def __make_url(self, path):
        url = "https://" + self.HOST + path
        return url
