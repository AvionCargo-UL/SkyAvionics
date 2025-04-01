from typing import List

import cv2
import numpy as np

from src.domain.vision.aruco.aruco import Aruco


class ArucoDrawer:

    CONTOUR_LINE_THICKNESS: int = 3
    CONTOUR_LINE_COLOR: tuple = (0, 255, 0)

    IDENTIFIER_TEXT_Y_OFFSET: int = 10

    FONT_SIZE: int = 1
    FONT_THICKNESS: int = 3
    FONT_COLOR: tuple = (255, 0, 0)

    AXIS_LENGTH: int = 10

    def __init__(self, camera_distortion: np.ndarray, camera_matrix: np.ndarray):
        self.__camera_distortion = camera_distortion
        self.__camera_matrix = camera_matrix

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

    def __draw_axis(self, image: cv2.Mat, aruco: Aruco):
        cv2.drawFrameAxes(
            image,
            self.__camera_matrix,
            self.__camera_distortion,
            aruco.angle.rotation_vector,
            aruco.angle.translation_vector,
            length=self.AXIS_LENGTH,
        )

    def __draw_detection_parameters(self, image: cv2.Mat, aruco: Aruco):
        # Base Y position
        y_pos = 50
        line_height = 50  # Vertical space between lines
        
        # Format rotation vector for better readability
        rot_vector = aruco.angle.rotation_vector
        rot_text = f"ROT: [{rot_vector[0]:.2f}, {rot_vector[1]:.2f}, {rot_vector[2]:.2f}]"
        
        # Format translation vector for better readability
        trans_vector = aruco.angle.translation_vector
        trans_text = f"TRS: [{trans_vector[0]:.2f}, {trans_vector[1]:.2f}, {trans_vector[2]:.2f}]"
        
        # Calculate distance
        distance = np.sqrt(np.sum(trans_vector**2))
        dist_text = f"DIST: {distance:.2f} units"
        
        # Draw each line separately
        cv2.putText(
            image,
            rot_text,
            (10, y_pos),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.FONT_SIZE,
            self.FONT_COLOR,
            self.FONT_THICKNESS,
        )
        
        y_pos += line_height
        cv2.putText(
            image,
            trans_text,
            (10, y_pos),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.FONT_SIZE,
            self.FONT_COLOR,
            self.FONT_THICKNESS,
        )
        
        y_pos += line_height
        cv2.putText(
            image,
            dist_text,
            (10, y_pos),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.FONT_SIZE,
            self.FONT_COLOR,
            self.FONT_THICKNESS,
        )

    def draw(self, image: cv2.Mat, arucos: List[Aruco]):
        for aruco in arucos:
            self.__draw_contour(image, aruco)
            self.__draw_identifier(image, aruco)
            self.__draw_axis(image, aruco)
            self.__draw_detection_parameters(image, aruco)
