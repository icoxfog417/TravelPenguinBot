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
        directions = []
        distance = Distance.Middle

        for t in generator.tokenize(text):
            pos = t.part_of_speech.split(",")
            if pos[0] == "名詞":
                d = self.__detect_direction(t)
                if d is not None:
                    directions.append(d)

        direction = self.__decide_direction(directions)
        return direction, distance

    def __decide_direction(self, directions):
        if len(directions) == 0:
            return None
        elif len([d for d in directions if d]) == 0:
            return None

        direction = None
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
