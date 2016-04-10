import json
from travel_penguin.server import Application
from tornado.testing import AsyncHTTPTestCase


class TestServer(AsyncHTTPTestCase):

    def get_app(self):
        return Application()

    def test_bot(self):
        j = get_test_json()
        response = self.fetch("/bot?debug=True", method="POST", body=j)
        self.assertEqual(response.code, 200)
        rb = json.loads(response.body.decode("utf-8"))
        self.assertEqual(rb["status"], True)


def get_test_json():
    msg = {
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
    return json.dumps(msg)
