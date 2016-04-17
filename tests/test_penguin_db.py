import unittest
import json
from travel_penguin.model.place import Place
from travel_penguin.travel.penguin_db import PenguinDb
from travel_penguin.env import Environment


class TestPenguinDb(unittest.TestCase):
    DB = None

    @classmethod
    def setUpClass(cls):
        env = Environment()
        db_url = env.get_database_url() + "_test"
        cls.DB = PenguinDb(db_url)

    @classmethod
    def tearDownClass(cls):
        cls.DB._drop()

    def test_visit(self):
        place = self.get_place()
        obj_id = self.DB.visit(place)
        self.assertTrue(obj_id)

        restored, time = self.DB.current()
        self.assertEqual(place.place_id, restored.place_id)


    def get_place(self):
        place = """
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
                }
            """

        p = Place.parse(json.loads(place))
        return p
