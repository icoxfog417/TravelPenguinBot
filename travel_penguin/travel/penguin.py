from enum import Enum
import math
import requests


class Direction(Enum):
    East = 0
    NorthEast = 45
    North = 90
    NorthWest = 135
    West = 180
    SouthWest = 225
    South = 270
    SouthEast = 325


class Distance(Enum):
    Long = 20000
    Middle = 10000
    Short = 5000


class Penguin():
    HOST = "https://maps.googleapis.com/maps/api/place"
    PLACES = "amusement_park|aquarium|art_gallery|bakery|bar|cafe|casino|convenience_store|library|movie_theater|restaurant|spa|stadium|university|zoo"

    def __init__(self, api_key, place):
        self.api_key = api_key
        self.place = place

    def move(self, direction: Direction, distance: Distance):
        lat, lng = self.place.move(direction, distance)

        new_ps = self.search(lat, lng)
        if len(new_ps) > 0:
            self.place = new_ps[0]
            return True
        else:
            return False

    def search(self, lat=-1.0, lng=-1.0, name=""):
        url = self.HOST + "/nearbysearch/json"
        _lat = lat if lat > 0 else self.place.lat
        _lng = lng if lng > 0 else self.place.lng

        params = {
            "key": self.api_key,
            "location": "{0},{1}".format(_lat, _lng),
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

    def get_current_place(self):
        "say current location"
        if self.place:
            return self.place
        else:
            ps = self.search()
            if len(ps) > 0:
                self.place = ps[0]
            return self.place

    def serialize(self):
        d = {
            "place": self.place.serialize()
        }
        return d

    @classmethod
    def deserialize(cls, api_key, status):
        place = status["place"]
        instance = Penguin(api_key, place)
        return instance


class Place():
    R = 6378150

    def __init__(self,
                 place_id,
                 lat,
                 lng,
                 name,
                 photos
                 ):
        self.place_id = place_id
        self.lat = lat
        self.lng = lng
        self.name = name
        self.photos = photos

    @classmethod
    def parse(cls, body):
        # see ref
        # https://developers.google.com/places/web-service/search?hl=ja#PlaceSearchResponses

        instance = Place(
            body["place_id"],
            body["geometry"]["location"]["lat"],
            body["geometry"]["location"]["lng"],
            body["name"],
            body["photos"]
        )

        return instance

    def move(self, direction: Direction, distance: Distance):
        y_unit = self.cal_m_per_lat()
        x_unit = self.cal_m_per_lng(self.lat)
        d = distance.value

        lat_unit = d / y_unit * math.sin(direction.value * math.pi / 180)
        lng_unit = d / x_unit * math.cos(direction.value * math.pi / 180)

        lat = self.lat + lat_unit
        lng = self.lng + lng_unit

        return lat, lng

    @classmethod
    def cal_m_per_lat(cls):
        circumference = 2 * math.pi * cls.R
        unit = circumference / 360
        return unit

    @classmethod
    def cal_m_per_lng(cls, lat):
        r_at_lat = cls.R * math.cos(abs(lat) / 180 * math.pi)
        c_at_lat = 2 * math.pi * r_at_lat
        unit = c_at_lat / 360
        return unit

    def serialize(self):
        d = self.__dict__
        return d

    @classmethod
    def deserialize(cls, obj):
        return Place(
            obj["place_id"],
            obj["lat"],
            obj["lng"],
            obj["name"],
            obj["photos"]
        )
