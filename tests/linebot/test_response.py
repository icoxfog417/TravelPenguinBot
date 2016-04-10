import unittest
import json
from linebot.models.line_response import LineResponse


class TestResponse(unittest.TestCase):

    def test_response(self):
        res = LineResponse("some_uesr")
        res.set_text("Hello")
        d = res.to_dict()
        self.assertEqual(d["content"]["text"], "Hello")

        j = json.dumps(d)
        self.assertTrue(len(j) > 0)
