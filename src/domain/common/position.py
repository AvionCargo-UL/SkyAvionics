class Position:
    def __init__(self, x: float, y: float):
        self.__x = x
        self.__y = y

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    def to_int_tuple(self) -> tuple[int, int]:
        return int(self.__x), int(self.__y)

    def __str__(self):
        return f"{self.__x}, {self.__y}"

    def __repr__(self):
        return f"Position({self.__x}, {self.__y})"
