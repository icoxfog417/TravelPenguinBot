from enum import Enum


class Direction(Enum):
    East = 0
    NorthEast = 45
    North = 90
    NorthWest = 135
    West = 180
    SouthWest = 225
    South = 270
    SouthEast = 325


class Distance(Enum):
    Long = 20000
    Middle = 10000
    Short = 5000
