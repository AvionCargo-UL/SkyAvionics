import numpy as np


class InvalidRotationMatrixException(RuntimeError):

    MESSAGE: str = "This is not a rotation matrix. %s"

    def __init__(self, matrix: np.ndarray):
        super().__init__(self.MESSAGE % matrix)
