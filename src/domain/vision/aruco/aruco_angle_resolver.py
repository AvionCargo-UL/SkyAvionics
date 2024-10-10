import math

import cv2
import numpy as np

from src.domain.common.angle import Angle
from src.domain.vision.exception.invalid_rotation_matrix_exception import (
    InvalidRotationMatrixException,
)


class ArucoAngleResolver:

    SINGULAR_MAGNITUDE_THRESHOLD: float = 1e-6
    MATRIX_SHAPE: int = 3

    def __init__(
        self, marker_size: int, camera_distortion: np.ndarray, camera_matrix: np.ndarray
    ):
        self.__marker_size: int = marker_size
        self.__camera_distortion: np.ndarray = camera_distortion
        self.__camera_matrix: np.ndarray = camera_matrix

        self.__flip_orientation: np.ndarray = self.__create_flip_orientation_matrix()

    def __create_flip_orientation_matrix(self) -> np.ndarray:
        flip_rotation_matrix = np.zeros(
            (self.MATRIX_SHAPE, self.MATRIX_SHAPE), dtype=np.float32
        )
        flip_rotation_matrix[0, 0] = 1.0
        flip_rotation_matrix[1, 1] = -1.0
        flip_rotation_matrix[2, 2] = -1.0
        return flip_rotation_matrix

    def __is_rotation_matrix(self, matrix: np.ndarray) -> bool:
        transpose_matrix = np.transpose(matrix)
        identity_approximation = np.dot(transpose_matrix, matrix)
        identity_matrix = np.identity(self.MATRIX_SHAPE, dtype=matrix.dtype)
        error_margin = np.linalg.norm(identity_matrix - identity_approximation)
        return error_margin < 1e-6

    def __is_singular_matrix(self, magnitude: float) -> bool:
        return magnitude < self.SINGULAR_MAGNITUDE_THRESHOLD

    def __rotation_matrix_to_angle(self, rotation_matrix: np.ndarray):
        if not self.__is_rotation_matrix(rotation_matrix):
            raise InvalidRotationMatrixException(rotation_matrix)

        magnitude = math.sqrt(
            rotation_matrix[0, 0] * rotation_matrix[0, 0]
            + rotation_matrix[1, 0] * rotation_matrix[1, 0]
        )

        if not self.__is_singular_matrix(magnitude):
            roll = math.atan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
            pitch = math.atan2(-rotation_matrix[2, 0], magnitude)
            yaw = math.atan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
        else:
            roll = math.atan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
            pitch = math.atan2(-rotation_matrix[2, 0], magnitude)
            yaw = 0

        return roll, pitch, yaw

    def __get_transposed_rotation_matrix(
        self, rotation_vector: np.ndarray
    ) -> np.ndarray:
        rotation_matrix = cv2.Rodrigues(rotation_vector)[0]
        return np.matrix(rotation_matrix).T

    def resolve(self, corners: np.ndarray) -> Angle:
        pose = cv2.aruco.estimatePoseSingleMarkers(
            corners, self.__marker_size, self.__camera_matrix, self.__camera_distortion
        )

        rotation_vector, translation_vector = pose[0][0, 0, :], pose[1][0, 0, :]
        transposed_matrix_rotation = self.__get_transposed_rotation_matrix(
            rotation_vector
        )

        roll, pitch, yaw = self.__rotation_matrix_to_angle(
            self.__flip_orientation * transposed_matrix_rotation
        )

        return Angle(roll, pitch, yaw, rotation_vector, translation_vector)
