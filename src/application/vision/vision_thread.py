import threading
import time
from typing import List

import cv2
from picamera2 import Picamera2
from queue import Queue

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
        self, camera_index: int, fps: float, vision_controller: VisionController, frame_queue: Queue
    ):
        threading.Thread.__init__(self)

        self.__camera_index = camera_index
        self.__thread_frequency_second = 1.0 / fps

        self.__vision_controller = vision_controller

        self.__frame_queue = frame_queue

        self.__stop_event = threading.Event()

        self.__picam = Picamera2()

        try:
            self.camera_config = self.__picam.create_preview_configuration()
            self.__picam.configure(self.camera_config)
            self.__picam.start()
        except Exception as e:
            print(f"Camera initialization failed: {e}")
            self.__stop_event.set()

    def __read_frame(self) -> cv2.Mat:

        try:
            frame = self.__picam.capture_array()
            return frame
        except Exception as e:
            print(f"Error reading frame: {e}")
            return None

    def run(self):
        while not self.__stop_event.is_set():
            frame = self.__read_frame()
            
            try:
                arucos: List[Aruco] = self.__vision_controller.do_aruco_detection(frame)
                self.__vision_controller.draw_aruco(frame, arucos)

                if not self.__frame_queue.full():
                    self.__frame_queue.put(frame)

            except InvalidRotationMatrixException as e:
                print(e)
            finally:
                time.sleep(self.__thread_frequency_second)

        self.dispose()

    def dispose(self):
        self.__picam.stop()

    def stop(self):
        self.__stop_event.set()
