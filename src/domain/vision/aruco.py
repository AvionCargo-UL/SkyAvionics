from src.domain.position import Position


class Aruco:
    def __init__(self, identifier: int, position: Position):
        self.__identifier = identifier
        self.__position = position

    @property
    def identifier(self) -> int:
        return self.__identifier

    def position(self) -> Position:
        return self.__position

    def __str__(self):
        return f"Identifier {self.__identifier}, {self.__position}"

    def __repr__(self):
        return f"Aruco({self.__identifier}, {self.__position})"
