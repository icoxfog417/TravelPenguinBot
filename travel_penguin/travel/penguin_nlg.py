# -*- coding: utf-8 -*-
from enum import Enum
from travel_penguin.model.move import Direction
from travel_penguin.model.act import ActionType
from travel_penguin.model.place import Place


class PenguinNLG():

    def __init__(self):
        pass

    def say(self, action_result, place: Place, direction):
        text = "あてもない旅さ・・・"
        if action_result == ActionType.describe:
           text = "俺の現在地は{0}だ。".format(place.name)
        elif action_result == ActionType.move:
            dt = self.__direction_to_text(direction)
            text = "俺は{0}へ旅をし、{1}にたどり着いた。".format(dt, place.name)
        elif action_result == ActionType.can_not_move:
            dt = self.__direction_to_text(direction)
            text = "ここから{0}へ進むことはできないようだ・・・戦略の練り直しが必要だな".format(dt)
        elif action_result == ActionType.can_not_understand:
            text = "ふむ・・・なかなか難しいね"

        return text

    def __direction_to_text(self, direction):
        text = "あてもない場所"
        if direction == Direction.North:
            text = "北"
        elif direction == Direction.NorthEast:
            text = "北東"
        elif direction == Direction.East:
            text = "東"
        elif direction == Direction.SouthEast:
            text = "南東"
        elif direction == Direction.South:
            text = "南"
        elif direction == Direction.SouthWest:
            text = "南西"
        elif direction == Direction.West:
            text = "西"
        elif direction == Direction.NorthWest:
            text = "北西"

        return text
