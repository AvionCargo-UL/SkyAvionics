from typing import List

import cv2

from src.domain.vision.aruco import Aruco
from src.domain.vision.aruco_detector import ArucoDetector


class VisionController:
    def __init__(self):
        self.__aruco_detector = ArucoDetector()

    def do_aruco_detection(self, image: cv2.Mat) -> List[Aruco]:
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return self.__aruco_detector.detect(grayscale_image)
