import json
from datetime import datetime
from pymongo import MongoClient
from travel_penguin.model.place import Place


class PenguinDb():
    PLACES = "places"
    TIMESTAMP_FIELD = "visited"

    def __init__(self, database_url):
        """
        database_url: have to include database name (mongodb://localhost:27017/your_db_name)
        """

        self.client = MongoClient(database_url)
        self.db = self.client.get_default_database()

    def visit(self, place: Place):
        collections = self.db[self.PLACES]
        obj = place.serialize()
        visited = datetime.utcnow()
        obj[self.TIMESTAMP_FIELD] = visited
        obj_id = collections.insert_one(obj)
        return visited

    def current(self):
        collections = self.db[self.PLACES]
        current = collections.find().sort(self.TIMESTAMP_FIELD, -1).limit(1)
        latest = list(current)
        if len(latest) == 1:
            c = latest[0]
            p = Place.deserialize(c)
            return p, c[self.TIMESTAMP_FIELD]
        else:
            return None, None

    def history(self, limit=100):
        collections = self.db[self.PLACES]
        history = collections.find().sort(self.TIMESTAMP_FIELD, -1).limit(limit)

        result = []
        for h in history:
            h["_id"] = str(h["_id"])
            h[self.TIMESTAMP_FIELD] = h[self.TIMESTAMP_FIELD].strftime("%Y/%m/%d %H:%M:%S")
            result.append(h)

        return result

    def _drop(self):
        collections = self.db[self.PLACES]
        collections.drop()
        self.client.drop_database(self.db.name)
