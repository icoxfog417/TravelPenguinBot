import math
from travel_penguin.model.move import Direction, Distance


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
            [] if "photos" not in body else body["photos"]
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
