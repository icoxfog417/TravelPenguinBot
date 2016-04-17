# -*- coding: utf-8 -*-
import datetime
from travel_penguin.model.act import CommandType, ActionType
from travel_penguin.travel.penguin_db import PenguinDb
from travel_penguin.travel.penguin_act import PenguinAct
from travel_penguin.travel.penguin_nlu import PenguinNLU
from travel_penguin.travel.penguin_nlg import PenguinNLG


class Penguin():

    def __init__(self, api_key, database_url):
        self.act = PenguinAct(api_key)
        self.db = PenguinDb(database_url)
        self.nlu = PenguinNLU()
        self.nlg = PenguinNLG()

        self.place = None
        self.visited = None
        self.place, self.visited = self.db.current()
        if self.place is None:
            self.__initialize()

    def __initialize(self):
        places = self.act.search(35.712195, 139.775220, "動物園")
        if len(places) == 0:
            raise Exception("Can not initialize first location")
        else:
            self.place = places[0]
            self.visited = self.db.visit(self.place)

    def ask(self, text):
        command = self.nlu.understand_command(text)

        if command == CommandType.move:
            return self.move(text)
        elif command == CommandType.describe:
            return self.describe(text)

    def describe(self, text):
        return ActionType.describe, self.nlg.say(ActionType.describe, self.place, None)

    def move(self, text):
        direction, distance = self.nlu.understand_move(text)
        result = ActionType.can_not_understand
        if direction is not None:
            new_place = self.act.move(self.place, direction, distance)
            if new_place is not None:
                self.place = new_place
                self.visited = self.db.visit(self.place)
                result = ActionType.move
            else:
                result = ActionType.can_not_move

        response = self.nlg.say(result, self.place, direction)

        return result, response
