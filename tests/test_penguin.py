import unittest
from travel_penguin.env import Environment
from travel_penguin.travel.penguin import Penguin
from travel_penguin.travel.penguin_nlg import ActionType


class TestPenguin(unittest.TestCase):
    PENGUIN = None

    @classmethod
    def setUpClass(cls):
        env = Environment()
        db_url = env.get_database_url() + "_test"
        cls.PENGUIN = Penguin(env.get_google_api_key(), db_url)

    @classmethod
    def tearDownClass(cls):
        cls.PENGUIN.db._drop()
        cls.PENGUIN = None

    def test_describe(self):
        text = "今どこにいるの"
        result_type, resp = self.PENGUIN.ask(text)
        self.assertEqual(ActionType.describe, result_type)
        print(resp)

    def test_move(self):
        text = "北西に進め"
        result_type, resp = self.PENGUIN.ask(text)
        self.assertEqual(ActionType.move, result_type)
        print(resp)

    def test_move_move(self):
        result_type, resp = self.PENGUIN.ask("北西に進め")
        self.assertEqual(ActionType.move, result_type)
        print(resp)

        result_type, resp = self.PENGUIN.ask("西へ行くんだ")
        self.assertEqual(ActionType.move, result_type)
        print(resp)

        result_type, resp = self.PENGUIN.ask("今どこ？")
        self.assertEqual(ActionType.describe, result_type)
        print(resp)
