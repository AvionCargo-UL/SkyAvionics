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
from src.domain.vision.vision_controller import VisionController


class VisionThread(threading.Thread):

    def __init__(
        self,
        camera_index: int,
        fps: float,
        vision_controller: VisionController,
        frame_queue: Queue,
        capture_width: int,
        capture_height: int,
    ):
        threading.Thread.__init__(self)

        self.__camera_index = camera_index
        self.__thread_frequency_second = 1.0 / fps
        self.__fps = fps
        self.__capture_resolution = (capture_width, capture_height)

        self.__vision_controller = vision_controller
        self.__frame_queue = frame_queue
        self.__stop_event = threading.Event()
        self.__picam = Picamera2()

        # Add a warmup period
        print("Camera warming up...")
        time.sleep(2)  # Give camera time to stabilize

        try:
            self.camera_config = self.__picam.create_preview_configuration(
                main={"size": self.__capture_resolution}
            )
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
            # Record the start time of this loop iteration
            loop_start_time = time.time()
            
            # Capture and process frame
            frame = self.__read_frame()

            if frame is None:
                time.sleep(self.__thread_frequency_second)
                continue

            try:
                # Use high-res frame for ArUco detection
                arucos: List[Aruco] = self.__vision_controller.do_aruco_detection(frame)
                self.__vision_controller.draw_aruco(frame, arucos)

                # Put frame in queue for other components
                if not self.__frame_queue.full():
                    self.__frame_queue.put(frame)
                
            except InvalidRotationMatrixException as e:
                print(e)
            
            # Calculate processing time and remaining sleep time
            processing_time = time.time() - loop_start_time
            sleep_time = max(0, self.__thread_frequency_second - processing_time)
            
            # Only sleep if needed to maintain cadence
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                # Optional: Log when we can't keep up with desired framerate
                print(f"Warning: Frame processing took {processing_time:.4f}s, exceeding target of {self.__thread_frequency_second:.4f}s")
                
            # Optional: Calculate and print actual FPS
            actual_frame_time = time.time() - loop_start_time
            actual_fps = 1.0 / actual_frame_time if actual_frame_time > 0 else 0
            if actual_fps < (self.__fps * 0.9):  # Only warn if significantly below target
                print(f"Actual FPS: {actual_fps:.2f}, Target: {self.__fps:.2f}")

        self.dispose()

    def dispose(self):
        self.__picam.stop()

    def stop(self):
        self.__stop_event.set()
        print("Stopping vision thread...")
        self.__picam.close()
