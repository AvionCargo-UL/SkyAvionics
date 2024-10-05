class Aruco:
    def __init__(self, identifier: int):
        self.__identifier = identifier

    def __str__(self):
        return f"Identifier {self.__identifier}"

    def __repr__(self):
        return f"Aruco({self.__identifier})"
