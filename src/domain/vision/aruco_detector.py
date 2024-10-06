from typing import List

import cv2

from src.domain.vision.aruco import Aruco
from src.domain.vision.aruco_factory import ArucoFactory


class ArucoDetector:
    def __init__(self):
        self.__aruco_factory = ArucoFactory()
        self.__aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.__parameters = cv2.aruco.DetectorParameters()

    def detect(self, grayscale_image: cv2.Mat) -> List[Aruco]:
        corners, ids, _ = cv2.aruco.detectMarkers(
            grayscale_image, self.__aruco_dict, parameters=self.__parameters
        )

        return [
            self.__aruco_factory.create(identifier, corner)
            for identifier, corner in zip(ids, corners)
        ]
