# -*- coding: utf-8 -*-
import unittest
from janome.tokenizer import Tokenizer
from travel_penguin.model.move import Direction
from travel_penguin.travel.penguin_nlu import PenguinNLU


class TestPenguinNLU(unittest.TestCase):

    def test_tokenize(self):
        generator = Tokenizer()
        text = "今どこ？　どこやねん? どこにいるの"
        for t in generator.tokenize(text):
            print(t)

    def test_understand_n(self):
        nlu = PenguinNLU()
        text = "北に向かうのだ"
        direction, _ = nlu.understand_move(text)
        self.assertEqual(Direction.North, direction)

    def test_understand_ne(self):
        nlu = PenguinNLU()
        text = "北と東に向かうのだ"
        direction, _ = nlu.understand_move(text)
        self.assertEqual(Direction.NorthEast, direction)

    def test_understand_e(self):
        nlu = PenguinNLU()
        text = "東に向かうのだ"
        direction, _ = nlu.understand_move(text)
        self.assertEqual(Direction.East, direction)

    def test_understand_se(self):
        nlu = PenguinNLU()
        text = "南東に向かうのだ"
        direction, _ = nlu.understand_move(text)
        self.assertEqual(Direction.SouthEast, direction)

    def test_understand_s(self):
        nlu = PenguinNLU()
        text = "南に行くのはいいぞ"
        direction, _ = nlu.understand_move(text)
        self.assertEqual(Direction.South, direction)

    def test_understand_sw(self):
        nlu = PenguinNLU()
        text = "南から西に向かうのだ"
        direction, _ = nlu.understand_move(text)
        self.assertEqual(Direction.SouthWest, direction)

    def test_understand_w(self):
        nlu = PenguinNLU()
        text = "西に向かうのだ"
        direction, _ = nlu.understand_move(text)
        self.assertEqual(Direction.West, direction)

    def test_understand_nw(self):
        nlu = PenguinNLU()
        text = "北西に向かうのだ"
        direction, _ = nlu.understand_move(text)
        self.assertEqual(Direction.NorthWest, direction)
