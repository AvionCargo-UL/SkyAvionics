from typing import List

import numpy as np

from src.domain.common.position import Position
from src.domain.vision.aruco.aruco import Aruco
from src.domain.vision.aruco.aruco_angle_resolver import ArucoAngleResolver


class ArucoFactory:
    def __init__(self, aruco_angle_resolver: ArucoAngleResolver):
        self.__aruco_angle_resolver = aruco_angle_resolver

    def __create_position(self, corners: np.ndarray) -> Position:
        position_x = float(np.mean(corners[0][:, 0]))
        position_y = float(np.mean(corners[0][:, 0]))
        return Position(position_x, position_y)

    def __create_corners(self, corners: np.ndarray) -> List[Position]:
        return [Position(x, y) for x, y in corners[0]]

    def create(self, identifier: int, corners: np.ndarray) -> Aruco:
        angle = self.__aruco_angle_resolver.resolve(corners)
        position = self.__create_position(corners)
        corners = self.__create_corners(corners)
        return Aruco(identifier, position, angle, corners)
