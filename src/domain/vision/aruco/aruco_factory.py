from typing import List

import numpy as np

from src.domain.common.position import Position
from src.domain.vision.aruco.aruco import Aruco


class ArucoFactory:
    def __init__(self):
        pass

    def __create_position(self, corners: List) -> Position:
        position_x: float = np.mean(corners[0][:, 0])
        position_y: float = np.mean(corners[0][:, 0])
        return Position(position_x, position_y)

    def create(self, identifier: int, corners: List) -> Aruco:
        position = self.__create_position(corners)
        return Aruco(identifier, position)
