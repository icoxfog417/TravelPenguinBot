import os
import json
from collections import namedtuple


class Environment():
    SECRET_TOKEN = "SECRET_TOKEN"
    GOOGLE_API_KEY = "GOOGLE_API_KEY"
    LINE_CHANNEL_ID = "LINE_CHANNEL_ID"
    LINE_CHANNEL_SECRET = "LINE_CHANNEL_SECRET"
    LINE_MID = "LINE_MID"
    DATABASE_URL = "MONGODB_URI" # for heroku
    PROXY = "FIXIE_URL"  # for heroku

    def __init__(self, key_file=""):
        self.key_file = os.path.join(os.path.dirname(__file__), "../" + (key_file if key_file else "keys.json"))
        self.keys = {}
        if os.path.isfile(self.key_file):
            with open(self.key_file, "r", encoding="utf-8") as f:
                self.keys = json.load(f)

    def get(self, keyname, alternative=""):
        key = os.environ.get(keyname)
        if not key and keyname in self.keys:
            key = self.keys[keyname]
        if not key:
            key = alternative

        return key

    def get_secret_token(self):
        return self.get(self.SECRET_TOKEN, "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__")

    def get_line_keys(self):
        keys = (self.get(self.LINE_CHANNEL_ID),
                self.get(self.LINE_CHANNEL_SECRET),
                self.get(self.LINE_MID))
        return keys

    def get_proxy(self):
        return self.get(self.PROXY)

    def get_google_api_key(self):
        return self.get(self.GOOGLE_API_KEY)

    def get_database_url(self):
        return self.get(self.DATABASE_URL)
