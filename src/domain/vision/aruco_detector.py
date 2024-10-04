from typing import List

import cv2

from src.domain.vision.aruco import Aruco


class ArucoDetector:
    def __init__(self):
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.parameters = cv2.aruco.DetectorParameters()

    def detect(self, grayscale_image: cv2.Mat) -> List[Aruco]:
        corners, ids, _ = cv2.aruco.detectMarkers(
            grayscale_image, self.aruco_dict, parameters=self.parameters
        )
        return [Aruco(identifier) for identifier in ids] if ids is not None else []
