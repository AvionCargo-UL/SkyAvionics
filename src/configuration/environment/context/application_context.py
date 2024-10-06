from abc import abstractmethod, ABC

from src.application.vision.vision_thread import VisionThread
from src.configuration.environment.application_configuration import (
    ApplicationConfiguration,
)
from src.configuration.service_locator import ServiceLocator
from src.domain.vision.exception.unable_to_read_frame_exception import (
    UnableToReadFrameException,
)


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
        ServiceLocator.register_dependency(
            VisionThread, self._instantiate_vision_thread()
        )

    @abstractmethod
    def _instantiate_vision_thread(self) -> VisionThread:
        pass
