import unittest
import json
from travel_penguin.travel.penguin_act import PenguinAct
from travel_penguin.model.move import Direction, Distance
from travel_penguin.model.place import Place
from travel_penguin.env import Environment


class TestPenguinAct(unittest.TestCase):

    def test_parse_places(self):
        places = self.get_test_places()
        parseds = [Place.parse(r) for r in places["results"]]
        self.assertTrue(len(parseds) > 0)

    def test_search(self):
        pa = self.create_penguin_act()
        places = pa.search(35.712195, 139.775220, "動物園")
        self.assertTrue(len(places) > 0)

    def test_move_penguin(self):
        pa = self.create_penguin_act()
        place = self.get_test_place()
        moved = pa.move(place, Direction.NorthEast, Distance.Long)
        self.assertTrue(moved)
        self.assertNotEquals(place.name, moved.name)
        self.assertTrue(moved.lat > place.lat)
        self.assertTrue(moved.lng > place.lng)

    def create_penguin_act(self) -> PenguinAct:
        env = Environment()
        api_key = env.get_google_api_key()
        penguin_act = PenguinAct(api_key)
        return penguin_act

    def get_test_place(self):
        place = Place.parse(self.get_test_places()["results"][0])
        return place

    def get_test_places(self):
        places = """
        {
            "html_attributions" : [],
            "results" : [
                {
                    "geometry" : {
                        "location" : {
                            "lat" : -33.870775,
                            "lng" : 151.199025
                        }
                    },
                    "icon" : "http://maps.gstatic.com/mapfiles/place_api/icons/travel_agent-71.png",
                    "id" : "21a0b251c9b8392186142c798263e289fe45b4aa",
                    "name" : "Rhythmboat Cruises",
                    "opening_hours" : {
                        "open_now" : true
                    },
                    "photos" : [
                        {
                            "height" : 270,
                            "html_attributions" : [],
                            "photo_reference" : "CnRnAAAAF-LjFR1ZV93eawe1cU_3QNMCNmaGkowY7CnOf-kcNmPhNnPEG9W979jOuJJ1sGr75rhD5hqKzjD8vbMbSsRnq_Ni3ZIGfY6hKWmsOf3qHKJInkm4h55lzvLAXJVc-Rr4kI9O1tmIblblUpg2oqoq8RIQRMQJhFsTr5s9haxQ07EQHxoUO0ICubVFGYfJiMUPor1GnIWb5i8",
                            "width" : 519
                        }
                    ],
                    "place_id" : "ChIJyWEHuEmuEmsRm9hTkapTCrk",
                    "scope" : "GOOGLE",
                    "alt_ids" : [
                        {
                            "place_id" : "D9iJyWEHuEmuEmsRm9hTkapTCrk",
                            "scope" : "APP"
                        }
                    ],
                    "reference" : "CoQBdQAAAFSiijw5-cAV68xdf2O18pKIZ0seJh03u9h9wk_lEdG-cP1dWvp_QGS4SNCBMk_fB06YRsfMrNkINtPez22p5lRIlj5ty_HmcNwcl6GZXbD2RdXsVfLYlQwnZQcnu7ihkjZp_2gk1-fWXql3GQ8-1BEGwgCxG-eaSnIJIBPuIpihEhAY1WYdxPvOWsPnb2-nGb6QGhTipN0lgaLpQTnkcMeAIEvCsSa0Ww",
                    "types" : [ "travel_agency", "restaurant", "food", "establishment" ],
                    "vicinity" : "Pyrmont Bay Wharf Darling Dr, Sydney"
                },
                {
                    "geometry" : {
                        "location" : {
                            "lat" : -33.870943,
                            "lng" : 151.190311
                        }
                    },
                    "icon" : "http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png",
                    "id" : "30bee58f819b6c47bd24151802f25ecf11df8943",
                    "name" : "Bucks Party Cruise",
                    "opening_hours" : {
                        "open_now" : true
                    },
                    "photos" : [
                        {
                            "height" : 600,
                            "html_attributions" : [],
                            "photo_reference" : "CnRnAAAA48AX5MsHIMiuipON_Lgh97hPiYDFkxx_vnaZQMOcvcQwYN92o33t5RwjRpOue5R47AjfMltntoz71hto40zqo7vFyxhDuuqhAChKGRQ5mdO5jv5CKWlzi182PICiOb37PiBtiFt7lSLe1SedoyrD-xIQD8xqSOaejWejYHCN4Ye2XBoUT3q2IXJQpMkmffJiBNftv8QSwF4",
                            "width" : 800
                        }
                    ],
                    "place_id" : "ChIJLfySpTOuEmsRsc_JfJtljdc",
                    "scope" : "GOOGLE",
                    "reference" : "CoQBdQAAANQSThnTekt-UokiTiX3oUFT6YDfdQJIG0ljlQnkLfWefcKmjxax0xmUpWjmpWdOsScl9zSyBNImmrTO9AE9DnWTdQ2hY7n-OOU4UgCfX7U0TE1Vf7jyODRISbK-u86TBJij0b2i7oUWq2bGr0cQSj8CV97U5q8SJR3AFDYi3ogqEhCMXjNLR1k8fiXTkG2BxGJmGhTqwE8C4grdjvJ0w5UsAVoOH7v8HQ",
                    "types" : [ "restaurant", "food", "establishment" ],
                    "vicinity" : "37 Bank St, Pyrmont"
                }
            ],
            "status" : "OK"
        }
        """
        return json.loads(places)
