class ContextConfigurationFilename:
    DEVELOPMENT: str = "dev-config.yaml"


class ApplicationConfigurationHeaderKey:
    VISION: str = "vision"
    MAVLINK_COMMUNICATION: str = "mavlink_communication"


class VisionConfigurationKey:
    CAMERA_INDEX: str = "camera_index"
    FPS: str = "fps"
    IMAGE_WIDTH: str = "image_width"
    IMAGE_HEIGHT: str = "image_height"
    FOCAL_LENGTH_MM: str = "focal_length_mm"
    PIXEL_SIZE_MM: str = "pixel_size_mm"
    MARKER_SIZE_MM: str = "marker_size_mm"

class MavlinkCommunicationConfigurationKey:
    DEVICE_STR: str = "device_string"
    REFRESH_RATE_S: str = "refresh_rate_s"
