class ContextConfigurationFilename:
    DEVELOPMENT: str = "dev-config.yaml"


class ApplicationConfigurationHeaderKey:
    VISION: str = "vision"
    ANTENNA_COMMUNICATION: str = "antenna_communication"


class VisionConfigurationKey:
    CAMERA_INDEX: str = "camera_index"
    FPS: str = "fps"
    IMAGE_WIDTH: str = "image_width"
    IMAGE_HEIGHT: str = "image_height"
    FOCAL_LENGTH_MM: str = "focal_length_mm"
    PIXEL_SIZE_MM: str = "pixel_size_mm"
    MARKER_SIZE: str = "marker_size"


class AntennaCommunicationConfigurationKey:
    REFRESH_RATE_S: str = "refresh_rate_s"
