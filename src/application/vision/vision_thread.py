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

    CAMERA_INDEX: int = 0
    THREAD_FREQUENCY_SECOND: float = 0.1

    def __init__(self):
        threading.Thread.__init__(self)

        self.__vision_controller = VisionController()
        self.__stop_event = threading.Event()
        self.__capture = cv2.VideoCapture(self.CAMERA_INDEX)

    def __read_frame(self) -> cv2.Mat:
        ret, frame = self.__capture.read()

        if not ret:
            raise UnableToReadFrameException(self.CAMERA_INDEX)

        return frame

    def run(self):
        while not self.__stop_event.is_set():
            frame = self.__read_frame()

            arucos: List[Aruco] = self.__vision_controller.do_aruco_detection(frame)
            if len(arucos) > 0:
                print(arucos)

            time.sleep(self.THREAD_FREQUENCY_SECOND)

        self.dispose()

    def dispose(self):
        self.__capture.release()

    def stop(self):
        self.__stop_event.set()
