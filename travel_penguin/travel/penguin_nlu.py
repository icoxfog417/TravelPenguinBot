# -*- coding: utf-8 -*-
from enum import Enum
from collections import Counter
from janome.tokenizer import Tokenizer
from travel_penguin.model.move import Direction, Distance
from travel_penguin.model.act import CommandType


class PenguinNLU():

    def __init__(self):
        pass

    def understand_command(self, text):
        command = CommandType.describe

        direction, distance = self.understand_move(text)
        if direction is not None and distance is not None:
            command = CommandType.move

        return command

    def understand_move(self, text):
        generator = Tokenizer()
        tokens = []

        for t in generator.tokenize(text):
            tokens.append(t)

        direction = self._understand_direction(tokens)
        distance = self._understand_distance(tokens)

        return direction, distance

    def _understand_direction(self, tokens):
        direction = None
        directions = []

        # gather direction descriptions
        for t in tokens:
            pos = t.part_of_speech.split(",")
            if pos[0] == "名詞":
                d = self.__detect_direction(t)
                if d is not None:
                    directions.append(d)

        # decide direction
        if len(directions) == 0:
            return None

        counts = Counter(directions)
        max_count = -1
        commons = []
        for d, c in counts.most_common():
            if max_count < 0:
                max_count = c
            if c == max_count:
                commons.append(d)
            else:
                break

        # merge direction
        if len(commons) > 1:
            if Direction.North in commons and Direction.East in commons:
                direction = Direction.NorthEast
            elif Direction.North in commons and Direction.West in commons:
                direction = Direction.NorthWest
            elif Direction.South in commons and Direction.East in commons:
                direction = Direction.SouthEast
            elif Direction.South in commons and Direction.West in commons:
                direction = Direction.SouthWest
        else:
            direction = commons[0]

        return direction

    def __detect_direction(self, t):
        direction = None
        if t.surface == "北":
            direction = Direction.North
        elif t.surface == "北東":
            direction = Direction.NorthEast
        elif t.surface == "東":
            direction = Direction.East
        elif t.surface == "南東":
            direction = Direction.SouthEast
        elif t.surface == "南":
            direction = Direction.South
        elif t.surface == "南西":
            direction = Direction.SouthWest
        elif t.surface == "西":
            direction = Direction.West
        elif t.surface == "北西":
            direction = Direction.NorthWest

        return direction

    def _understand_distance(self, tokens):
        Shorts = ["チョット", "イッシュン", "ワズカニ"]
        Longs = ["スゴク", "デカク", "ハルカニ", "タクサン"]
        distances = []
        distance = Distance.Middle

        for t in tokens:
            pos = t.part_of_speech.split(",")
            target = False
            if pos[0] == "形容詞":
                target = True
            if pos[1] == "形容動詞語幹":
                target = True
            elif pos[0] == "副詞":
                target = True
            elif pos[0] == "名詞" and pos[1] == "副詞可能":
                target = True

            if target:
                if t.reading in Shorts or sum(w in t.surface for w in ["小", "短"]) > 0:
                    distances.append(Distance.Short)
                elif t.reading in Longs or sum(w in t.surface for w in ["大", "長"]) > 0:
                    distances.append(Distance.Long)

        if len(distances) > 0:
            counts = Counter(distances)
            distance = counts.most_common(1)[0][0]

        return distance
