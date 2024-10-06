from typing import List

import cv2

from src.domain.vision.aruco.aruco import Aruco


class ArucoDrawer:

    CONTOUR_LINE_THICKNESS: int = 3
    CONTOUR_LINE_COLOR: tuple = (0, 255, 0)

    IDENTIFIER_TEXT_Y_OFFSET: int = 10

    FONT_SIZE: int = 1
    FONT_THICKNESS: int = 3
    FONT_COLOR: tuple = (255, 0, 0)

    def __init__(self):
        pass

    def __draw_contour(self, image: cv2.Mat, aruco: Aruco):
        cv2.line(
            image,
            aruco.top_left.to_int_tuple(),
            aruco.top_right.to_int_tuple(),
            self.CONTOUR_LINE_COLOR,
            self.CONTOUR_LINE_THICKNESS,
        )
        cv2.line(
            image,
            aruco.top_right.to_int_tuple(),
            aruco.bottom_right.to_int_tuple(),
            self.CONTOUR_LINE_COLOR,
            self.CONTOUR_LINE_THICKNESS,
        )
        cv2.line(
            image,
            aruco.bottom_right.to_int_tuple(),
            aruco.bottom_left.to_int_tuple(),
            self.CONTOUR_LINE_COLOR,
            self.CONTOUR_LINE_THICKNESS,
        )
        cv2.line(
            image,
            aruco.bottom_left.to_int_tuple(),
            aruco.top_left.to_int_tuple(),
            self.CONTOUR_LINE_COLOR,
            self.CONTOUR_LINE_THICKNESS,
        )

    def __draw_identifier(self, image: cv2.Mat, aruco: Aruco):
        cv2.putText(
            image,
            str(aruco.identifier),
            (
                int(aruco.top_left.x),
                int(aruco.top_left.y - self.IDENTIFIER_TEXT_Y_OFFSET),
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.FONT_SIZE,
            self.FONT_COLOR,
            self.FONT_THICKNESS,
        )

    def draw(self, image: cv2.Mat, arucos: List[Aruco]):
        for aruco in arucos:
            self.__draw_contour(image, aruco)
            self.__draw_identifier(image, aruco)
