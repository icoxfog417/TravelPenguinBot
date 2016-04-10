import unittest
from linebot.models.line_request import LineRequest


class TestRequest(unittest.TestCase):

    def test_request_parse(self):
        req = get_test_message()
        requests = LineRequest.parse(req)
        self.assertEqual(len(requests), 1)


def get_test_message():
    return {
        "result":[
            {
                "from":"u206d25c2ea6bd87c17655609a1c37cb8",
                "fromChannel":"1341301815",
                "to":["u0cc15697597f61dd8b01cea8b027050e"],
                "toChannel":"1441301333",
                "eventType":"138311609000106303",
                "id":"ABCDEF-12345678901",
                "content": {
                    "location": None,
                    "id":"325708",
                    "contentType":1,
                    "from":"uff2aec188e58752ee1fb0f9507c6529a",
                    "createdTime":1332394961610,
                    "to":["u0a556cffd4da0dd89c94fb36e36e1cdc"],
                    "toType":1,
                    "contentMetadata": None,
                    "text":"Hello, BOT API Server!"
                }
            }
        ]
    }