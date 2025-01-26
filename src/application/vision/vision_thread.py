import threading
import time
from typing import List

import cv2

from src.domain.vision.aruco.aruco import Aruco
from src.domain.vision.exception.invalid_rotation_matrix_exception import (
    InvalidRotationMatrixException,
)
from src.domain.vision.exception.unable_to_read_frame_exception import (
    UnableToReadFrameException,
)
from src.domain.vision.vision_controller import VisionController


class VisionThread(threading.Thread):

    def __init__(
        self, camera_index: int, fps: float, vision_controller: VisionController
    ):
        threading.Thread.__init__(self)

        self.__camera_index = camera_index
        self.__thread_frequency_second = 1.0 / fps

        self.__vision_controller = vision_controller

        self.__stop_event = threading.Event()
        self.__capture = cv2.VideoCapture(self.__camera_index)

    def __read_frame(self) -> cv2.Mat:
        # TODO : Change the capture from computer to RPI
        ret, frame = self.__capture.read()

        if not ret:
            raise UnableToReadFrameException(self.__camera_index)

        return frame

    def run(self):
        while not self.__stop_event.is_set():
            frame = self.__read_frame()

            try:
                arucos: List[Aruco] = self.__vision_controller.do_aruco_detection(frame)
                self.__vision_controller.draw_aruco(frame, arucos)

                # TODO : Send the frame to the GCS

            except InvalidRotationMatrixException as e:
                print(e)
            finally:
                time.sleep(self.__thread_frequency_second)

        self.dispose()

    def dispose(self):
        self.__capture.release()

    def stop(self):
        self.__stop_event.set()
