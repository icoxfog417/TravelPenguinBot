from enum import Enum


class CommandType():
    describe = 0
    move = 1


class ActionType(Enum):
    describe = 1
    move = 2
    can_not_move = 2
    can_not_understand = 3
