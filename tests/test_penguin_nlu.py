# -*- coding: utf-8 -*-
import unittest
from janome.tokenizer import Tokenizer
from travel_penguin.model.move import Direction, Distance
from travel_penguin.travel.penguin_nlu import PenguinNLU


class TestPenguinNLU(unittest.TestCase):

    def test_tokenize(self):
        generator = Tokenizer()
        text = "北東へちょっと小さく移動"
        for t in generator.tokenize(text):
            print(t)

    def test_directions(self):
        self.assertDirection("北に向かうのだ", Direction.North)
        self.assertDirection("北と東に向かうのだ", Direction.NorthEast)
        self.assertDirection("東に向かうのだ", Direction.East)
        self.assertDirection("南東に向かうのだ", Direction.SouthEast)
        self.assertDirection("南に行くのはいいぞ", Direction.South)
        self.assertDirection("南から西に向かうのだ", Direction.SouthWest)
        self.assertDirection("西に向かうのだ", Direction.West)
        self.assertDirection("北西に向かうのだ", Direction.NorthWest)

    def test_distance(self):
        self.assertDistance("大きく移動", Distance.Long)
        self.assertDistance("長く移動", Distance.Long)
        self.assertDistance("すごく移動", Distance.Long)
        self.assertDistance("小さめに移動", Distance.Short)
        self.assertDistance("ちょっとだけ移動", Distance.Short)
        self.assertDistance("短く移動", Distance.Short)
        self.assertDistance("移動", Distance.Middle)
        self.assertDistance("とりあえず移動", Distance.Middle)

    def assertDirection(self, text, direction):
        nlu = PenguinNLU()
        _dr, _ds = nlu.understand_move(text)
        self.assertEqual(_dr, direction)

    def assertDistance(self, text, distance):
        nlu = PenguinNLU()
        _dr, _ds = nlu.understand_move(text)
        self.assertEqual(_ds, distance)
