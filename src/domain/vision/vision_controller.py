from typing import List

import cv2

from src.domain.vision.aruco.aruco_drawer import ArucoDrawer
from src.domain.vision.aruco.aruco_factory import Aruco
from src.domain.vision.aruco.aruco_detector import ArucoDetector


class VisionController:
    def __init__(self, aruco_detector: ArucoDetector, aruco_drawer: ArucoDrawer):
        self.__aruco_detector = aruco_detector
        self.__aruco_drawer = aruco_drawer

    def do_aruco_detection(self, image: cv2.Mat) -> List[Aruco]:
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return self.__aruco_detector.detect(grayscale_image)

    def draw_aruco(self, frame: cv2.Mat, arucos: List[Aruco]):
        self.__aruco_drawer.draw(frame, arucos)
