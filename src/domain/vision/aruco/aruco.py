from typing import List

from src.domain.common.position import Position


class Aruco:
    def __init__(self, identifier: int, position: Position, corners: List[Position]):
        self.__identifier = identifier
        self.__position = position
        self.__corners = corners

    @property
    def identifier(self) -> int:
        return self.__identifier

    @property
    def position(self) -> Position:
        return self.__position

    @property
    def top_left(self) -> Position:
        return self.__corners[0]

    @property
    def top_right(self) -> Position:
        return self.__corners[1]

    @property
    def bottom_right(self) -> Position:
        return self.__corners[2]

    @property
    def bottom_left(self) -> Position:
        return self.__corners[3]

    def __str__(self):
        return f"{self.__identifier}, {self.__position}, {self.__corners}"

    def __repr__(self):
        return f"Aruco({self.__identifier}, {repr(self.__position)}, {repr(self.__corners)})"
