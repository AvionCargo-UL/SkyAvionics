from abc import abstractmethod, ABC
from queue import Queue
from typing import List
import time

import numpy as np
from pymavlink import mavutil

from src.application.mavlink.mavlink_service import MavlinkThread
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

from src.interfaces.api.fast_api_thread import FastAPIThread


class ApplicationContext(ABC):

    def __init__(self, filepath: str):
        self._configuration = ApplicationConfiguration(filepath)

    def start_application(self):

        state_machine: StateMachine = ServiceLocator.get_dependency(StateMachine)
        mavlink_thread: MavlinkThread = ServiceLocator.get_dependency(MavlinkThread)

        vision_thread: VisionThread = ServiceLocator.get_dependency(VisionThread)
        fast_api_thread: FastAPIThread = ServiceLocator.get_dependency(FastAPIThread)

        vision_thread.start()
        fast_api_thread.start()

        while True:
            state_machine.execute()
            time.sleep(1)

        try:
            fast_api_thread.join()
            vision_thread.join()
        except UnableToReadFrameException as e:
            print(e)
        finally:
            vision_thread.dispose()
            fast_api_thread.dispose()

    def build_application(self):
        ServiceLocator.clear()

        states: dict[StateEnum, State] = {
            StateEnum.IDLE: Idle(),
            StateEnum.TAKEOFF: Takeoff(),
            StateEnum.FLY: Fly(0.25),
            StateEnum.DETECT_ARUCO: DetectAruco(),
        }
        state_machine = StateMachine(states, StateEnum.TAKEOFF)

        send_frame_queue = Queue()
        send_telemetry_queue = Queue()
        response_queue = Queue()

        camera_distortion = self._load_camera_distortion()
        camera_matrix = self._load_camera_matrix()

        vision_controller = self._instantiate_vision_controller(
            camera_distortion, camera_matrix
        )

        ServiceLocator.register_dependency(
            VisionThread,
            self._instantiate_vision_thread(vision_controller, send_frame_queue),
        )

        ServiceLocator.register_dependency(
            FastAPIThread,
            self._instantiate_fast_API_thread(
                send_frame_queue, send_telemetry_queue, response_queue
            ),
        )

        ServiceLocator.register_dependency(
           MavlinkThread, self._instantiate_mavlink_service("COM5", 
                                                            115200, # Baudrate
                                                            5000, # Timeout
                                                            3, # Retries
                                                            self._configuration.mavlink_communication_refresh_rate_s, # Refresh rate
                                                            )
        )

        ServiceLocator.register_dependency(StateMachine, state_machine)

    @abstractmethod
    def _instantiate_vision_thread(
        self, vision_controller: VisionController, send_frame_queue: Queue
    ) -> VisionThread:
        pass

    @abstractmethod
    def _instantiate_fast_API_thread(
        self,
        send_frame_queue: Queue,
        send_telemetry_queue: Queue,
        response_queue=Queue,
    ) -> FastAPIThread:
        pass

    @abstractmethod
    def _instantiate_vision_controller(
        self, camera_distortion: np.ndarray, camera_matrix: np.ndarray
    ) -> VisionController:
        pass

    @abstractmethod
    def _instantiate_mavlink_service(
        self, device: str, baudrate: int, timeout_ms: int, retries: int, refresh_rate_s : float,
    ) -> MavlinkThread:
        pass

    @abstractmethod
    def _load_camera_distortion(self) -> np.ndarray:
        pass

    @abstractmethod
    def _load_camera_matrix(self) -> np.ndarray:
        pass
