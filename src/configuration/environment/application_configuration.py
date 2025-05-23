import yaml

from src.configuration.environment.constant import (
    ApplicationConfigurationHeaderKey,
    VisionConfigurationKey,
    MavlinkCommunicationConfigurationKey,
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

    def __get_str(self, header: str, variable_name: str) -> str:
        return str(self.__get_variable(header, variable_name))

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

    @property
    def vision_image_width(self) -> int:
        return self.__get_int(
            ApplicationConfigurationHeaderKey.VISION,
            VisionConfigurationKey.IMAGE_WIDTH,
        )

    @property
    def vision_image_height(self) -> int:
        return self.__get_int(
            ApplicationConfigurationHeaderKey.VISION,
            VisionConfigurationKey.IMAGE_HEIGHT,
        )

    @property
    def vision_focal_length_mm(self) -> float:
        return self.__get_float(
            ApplicationConfigurationHeaderKey.VISION,
            VisionConfigurationKey.FOCAL_LENGTH_MM,
        )

    @property
    def vision_pixel_size_mm(self) -> float:
        return self.__get_float(
            ApplicationConfigurationHeaderKey.VISION,
            VisionConfigurationKey.PIXEL_SIZE_MM,
        )

    @property
    def vision_marker_size_mm(self) -> int:
        return self.__get_int(
            ApplicationConfigurationHeaderKey.VISION, VisionConfigurationKey.MARKER_SIZE_MM
        )
    
    @property
    def mavlink_device_string(self) -> float:
        return self.__get_str(
            ApplicationConfigurationHeaderKey.MAVLINK_COMMUNICATION,
            MavlinkCommunicationConfigurationKey.DEVICE_STR,
        )

    @property
    def mavlink_communication_refresh_rate_s(self) -> float:
        return self.__get_float(
            ApplicationConfigurationHeaderKey.MAVLINK_COMMUNICATION,
            MavlinkCommunicationConfigurationKey.REFRESH_RATE_S,
        )

