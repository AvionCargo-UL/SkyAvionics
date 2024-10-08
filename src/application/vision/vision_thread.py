import threading
import time
from typing import List

import cv2

from src.domain.vision.aruco.aruco import Aruco
from src.domain.vision.exception.unable_to_read_frame_exception import (
    UnableToReadFrameException,
)
from src.domain.vision.vision_controller import VisionController


class VisionThread(threading.Thread):

    def __init__(self, camera_index: int, thread_frequency_second: float):
        threading.Thread.__init__(self)

        self.__camera_index = camera_index
        self.__thread_frequency_second = thread_frequency_second

        self.__vision_controller = VisionController()

        self.__stop_event = threading.Event()
        self.__capture = cv2.VideoCapture(self.__camera_index)

    def __read_frame(self) -> cv2.Mat:
        ret, frame = self.__capture.read()

        if not ret:
            raise UnableToReadFrameException(self.__camera_index)

        return frame

    def run(self):
        while not self.__stop_event.is_set():
            frame = self.__read_frame()

            arucos: List[Aruco] = self.__vision_controller.do_aruco_detection(frame)
            self.__vision_controller.draw_on_aruco(frame, arucos)

            time.sleep(self.__thread_frequency_second)

        self.dispose()

    def dispose(self):
        self.__capture.release()

    def stop(self):
        self.__stop_event.set()
