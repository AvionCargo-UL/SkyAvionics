from src.application.vision.vision_thread import VisionThread
from src.configuration.environment.constant import ContextConfigurationFilename
from src.configuration.environment.context.application_context import ApplicationContext


class DevelopmentContext(ApplicationContext):
    def __init__(self):
        super().__init__(ContextConfigurationFilename.DEVELOPMENT)

    def _instantiate_vision_thread(self) -> VisionThread:
        return VisionThread(
            self._configuration.vision_camera_index,
            self._configuration.vision_thread_frequency,
        )
