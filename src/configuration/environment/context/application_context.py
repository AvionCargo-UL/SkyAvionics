from abc import abstractmethod, ABC

import numpy as np

from src.application.vision.vision_thread import VisionThread
from src.configuration.environment.application_configuration import (
    ApplicationConfiguration,
)
from src.configuration.service_locator import ServiceLocator
from src.domain.vision.exception.unable_to_read_frame_exception import (
    UnableToReadFrameException,
)
from src.domain.vision.vision_controller import VisionController


class ApplicationContext(ABC):
    def __init__(self, filepath: str):
        self._configuration = ApplicationConfiguration(filepath)

    def start_application(self):
        vision_thread: VisionThread = ServiceLocator.get_dependency(VisionThread)
        vision_thread.start()

        try:
            vision_thread.join()
        except UnableToReadFrameException as e:
            print(e)
        finally:
            vision_thread.dispose()

    def build_application(self):
        ServiceLocator.clear()

        camera_distortion = self._load_camera_distortion()
        camera_matrix = self._load_camera_matrix()

        vision_controller = self._instantiate_vision_controller(
            camera_distortion, camera_matrix
        )

        ServiceLocator.register_dependency(
            VisionThread, self._instantiate_vision_thread(vision_controller)
        )

    @abstractmethod
    def _instantiate_vision_thread(
        self, vision_controller: VisionController
    ) -> VisionThread:
        pass

    @abstractmethod
    def _instantiate_vision_controller(
        self, camera_distortion: np.ndarray, camera_matrix: np.ndarray
    ) -> VisionController:
        pass

    @abstractmethod
    def _load_camera_distortion(self) -> np.ndarray:
        pass

    @abstractmethod
    def _load_camera_matrix(self) -> np.ndarray:
        pass
