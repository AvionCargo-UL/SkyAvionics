from enum import auto, Enum


class StateEnum(Enum):
    IDLE = (auto(),)
    FLY = (auto(),)
    TAKEOFF = (auto(),)
    DETECT_ARUCO = (auto(),)
