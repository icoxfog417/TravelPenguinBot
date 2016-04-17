import requests
from travel_penguin.model.move import Direction, Distance
from travel_penguin.model.place import Place


class PenguinAct():
    HOST = "https://maps.googleapis.com/maps/api/place"
    PLACES = "amusement_park|aquarium|art_gallery|bakery|bar|cafe|casino|convenience_store|library|movie_theater|restaurant|spa|stadium|university|zoo"

    def __init__(self, api_key):
        self.api_key = api_key

    def move(self, place, direction: Direction, distance: Distance):
        lat, lng = place.move(direction, distance)

        new_ps = self.search(lat, lng)
        if len(new_ps) > 0:
            return new_ps[0]
        else:
            return None

    def search(self, lat, lng, name=""):
        url = self.HOST + "/nearbysearch/json"

        params = {
            "key": self.api_key,
            "location": "{0},{1}".format(lat, lng),
            "radius": 5000,
            "types": self.PLACES
        }
        if name:
            params["name"] = name

        r = requests.get(url, params=params)
        places = []
        if not r.ok:
            r.raise_for_status()
        else:
            body = r.json()
            if "status" in body and body["status"] != "OK":
                raise Exception("Can not retreave places.")
            else:
                results = body["results"]
                places = [Place.parse(p) for p in results]

        return places
