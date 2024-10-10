import numpy as np


class Angle:
    def __init__(
        self,
        roll: float,
        pitch: float,
        yaw: float,
        rotation_vector: np.ndarray,
        translation_vector: np.ndarray,
    ):
        self.roll: float = roll
        self.pitch: float = pitch
        self.yaw: float = yaw
        self.rotation_vector: np.ndarray = rotation_vector
        self.translation_vector: np.ndarray = translation_vector
