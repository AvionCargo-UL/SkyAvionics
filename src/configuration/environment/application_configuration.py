import yaml

from src.configuration.environment.constant import (
    ApplicationConfigurationHeaderKey,
    VisionConfigurationKey,
)
from src.configuration.environment.exception.application_variable_not_found_exception import (
    ApplicationVariableNotFoundException,
)


class ApplicationConfiguration:
    def __init__(self, file_path: str):
        with open(file_path, "r") as file:
            self.__configuration = yaml.safe_load(file)

    def __get_variable(self, header: str, variable_name: str):
        try:
            return self.__configuration[header][variable_name]
        except (KeyError, ValueError):
            raise ApplicationVariableNotFoundException(header, variable_name)

    def __get_int(self, header: str, variable_name: str) -> int:
        return int(self.__get_variable(header, variable_name))

    def __get_float(self, header: str, variable_name: str) -> float:
        return float(self.__get_variable(header, variable_name))

    @property
    def vision_camera_index(self) -> int:
        return self.__get_int(
            ApplicationConfigurationHeaderKey.VISION,
            VisionConfigurationKey.CAMERA_INDEX,
        )

    @property
    def vision_fps(self) -> int:
        return self.__get_int(
            ApplicationConfigurationHeaderKey.VISION,
            VisionConfigurationKey.FPS,
        )
