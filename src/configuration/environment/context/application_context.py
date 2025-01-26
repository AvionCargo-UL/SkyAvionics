from abc import abstractmethod, ABC
from queue import Queue
from typing import List

import numpy as np
from pymavlink import mavutil

from src.application.communication.antenna_communication_thread import (
    AntennaCommunicationThread,
)
from src.application.mavlink.mavlink_service import MavlinkService
from src.application.vision.vision_thread import VisionThread
from src.configuration.environment.application_configuration import (
    ApplicationConfiguration,
)
from src.configuration.service_locator import ServiceLocator
from src.domain.mavlink.mavlink_mission_item import MavlinkMissionItem
from src.domain.state_machine.state import State
from src.domain.state_machine.state_machine import StateMachine


from src.domain.state_machine.states.idle import Idle

from src.domain.state_machine.states.takeoff import Takeoff

from src.domain.state_machine.states.fly import Fly

from src.domain.state_machine.states.detect_aruco import DetectAruco
from src.domain.state_machine.states_enum import StateEnum
from src.domain.vision.exception.unable_to_read_frame_exception import (
    UnableToReadFrameException,
)
from src.domain.vision.vision_controller import VisionController


class ApplicationContext(ABC):
    """
    My first little commit !
    """

    def __init__(self, filepath: str):
        self._configuration = ApplicationConfiguration(filepath)

    def start_application(self):

        state_machine: StateMachine = ServiceLocator.get_dependency(StateMachine)
        mavlink_service: MavlinkService = ServiceLocator.get_dependency(MavlinkService)

        mission_items: List[MavlinkMissionItem] = [
            MavlinkMissionItem(
                0,
                0,
                0,
                mavutil.mavlink.MAV_FRAME_GLOBAL,
                mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                0,
                0,
                1,
                0,
                0,
                0,
                37.874,
                -122.262,
                0,
            ),  # Home
            MavlinkMissionItem(
                0,
                0,
                1,
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                0,
                0,
                0,
                0,
                0,
                0,
                37.874,
                -122.262,
                1,
            ),  # Takeoff
            MavlinkMissionItem(
                0,
                0,
                2,
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                0,
                0,
                0,
                0,
                0,
                0,
                37.874,
                -122.5,
                20,
            ),  # Waypoint 2
            MavlinkMissionItem(
                0,
                0,
                3,
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                0,
                0,
                0,
                0,
                0,
                0,
                37.8,
                -122.259,
                20,
            ),  # Waypoint 3
            MavlinkMissionItem(
                0,
                0,
                4,
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                mavutil.mavlink.MAV_CMD_NAV_LAND,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ),  # Return to launch
        ]

        mavlink_service.upload_mission(mission_items)

        vision_thread: VisionThread = ServiceLocator.get_dependency(VisionThread)
        antenna_communication_thread: AntennaCommunicationThread = (
            ServiceLocator.get_dependency(AntennaCommunicationThread)
        )

        vision_thread.start()
        antenna_communication_thread.start()

        while True:
            state_machine.execute()

        try:
            antenna_communication_thread.join()
            vision_thread.join()
        except UnableToReadFrameException as e:
            print(e)
        finally:
            vision_thread.dispose()

    def build_application(self):
        ServiceLocator.clear()

        states: dict[StateEnum, State] = {
            StateEnum.IDLE: Idle(),
            StateEnum.TAKEOFF: Takeoff(),
            StateEnum.FLY: Fly(0.25),
            StateEnum.DETECT_ARUCO: DetectAruco(),
        }
        state_machine = StateMachine(states, StateEnum.TAKEOFF)

        send_queue = Queue()
        response_queue = Queue()

        camera_distortion = self._load_camera_distortion()
        camera_matrix = self._load_camera_matrix()

        vision_controller = self._instantiate_vision_controller(
            camera_distortion, camera_matrix
        )

        ServiceLocator.register_dependency(
            VisionThread, self._instantiate_vision_thread(vision_controller)
        )

        ServiceLocator.register_dependency(
            AntennaCommunicationThread,
            self._instantiate_antenna_communication_thread(send_queue, response_queue),
        )

        ServiceLocator.register_dependency(
            MavlinkService, self._instantiate_mavlink_service("COM5", 115200, 5000, 3)
        )

        ServiceLocator.register_dependency(StateMachine, state_machine)

    @abstractmethod
    def _instantiate_antenna_communication_thread(
        self, send_queue: Queue, response_queue: Queue
    ) -> AntennaCommunicationThread:
        pass

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
    def _instantiate_mavlink_service(
        self, port: str, baudrate: int, timeout_ms: int, retries: int
    ) -> MavlinkService:
        pass

    @abstractmethod
    def _load_camera_distortion(self) -> np.ndarray:
        pass

    @abstractmethod
    def _load_camera_matrix(self) -> np.ndarray:
        pass
