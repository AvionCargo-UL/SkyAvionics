from queue import Queue

import numpy as np

from src.application.communication.antenna_communication_thread import (
    AntennaCommunicationThread,
)
from src.application.mavlink.mavlink_service import MavlinkService
from src.application.vision.vision_thread import VisionThread
from src.configuration.environment.constant import ContextConfigurationFilename
from src.configuration.environment.context.application_context import ApplicationContext
from src.domain.vision.aruco.aruco_angle_resolver import ArucoAngleResolver
from src.domain.vision.aruco.aruco_detector import ArucoDetector
from src.domain.vision.aruco.aruco_drawer import ArucoDrawer
from src.domain.vision.aruco.aruco_factory import ArucoFactory
from src.domain.vision.vision_controller import VisionController


class DevelopmentContext(ApplicationContext):
    def __init__(self):
        super().__init__(ContextConfigurationFilename.DEVELOPMENT)

    def _instantiate_antenna_communication_thread(
        self, send_queue: Queue, response_queue: Queue
    ) -> AntennaCommunicationThread:
        return AntennaCommunicationThread(
            self._configuration.antenna_communication_refresh_rate_s,
            send_queue,
            response_queue,
        )

    def _instantiate_vision_thread(
        self, vision_controller: VisionController
    ) -> VisionThread:
        return VisionThread(
            self._configuration.vision_camera_index,
            self._configuration.vision_fps,
            vision_controller,
        )

    def _instantiate_vision_controller(
        self, camera_distortion: np.ndarray, camera_matrix: np.ndarray
    ) -> VisionController:
        aruco_angle_resolver = ArucoAngleResolver(
            self._configuration.vision_marker_size, camera_distortion, camera_matrix
        )
        aruco_factory = ArucoFactory(aruco_angle_resolver)
        aruco_detector = ArucoDetector(aruco_factory)
        aruco_drawer = ArucoDrawer(camera_distortion, camera_matrix)
        return VisionController(aruco_detector, aruco_drawer)

    def _instantiate_mavlink_service(
        self, port: str, baudrate: int, timeout_ms: int, retries: int
    ) -> MavlinkService:
        return MavlinkService(port, baudrate, timeout_ms, retries)

    def _load_camera_distortion(self) -> np.ndarray:
        return np.array([0, 0, 0, 0], dtype=np.float32)

    def _load_camera_matrix(self) -> np.ndarray:
        width, height = (
            self._configuration.vision_image_width,
            self._configuration.vision_image_height,
        )

        focal_length_x = focal_length_y = (
            self._configuration.vision_focal_length_mm
            / self._configuration.vision_pixel_size_mm
        )

        center_x = width / 2
        center_y = height / 2

        return np.array(
            [[focal_length_x, 0, center_x], [0, focal_length_y, center_y], [0, 0, 1]],
            dtype=np.float32,
        )
