from datetime import datetime

from src.domain.state_machine.state import State
from src.domain.state_machine.states_enum import StateEnum


class Fly(State):

    def __init__(self, flight_duration_sec: float):
        self.__flight_duration = flight_duration_sec
        self.__start_time = datetime.now()

    def on_enter(self):
        print("Fly - on_enter")
        self.__start_time = datetime.now()

    def execute(self) -> StateEnum:
        flight_time = float((datetime.now() - self.__start_time).total_seconds())
        if flight_time > self.__flight_duration:
            return StateEnum.DETECT_ARUCO

    def on_exit(self):
        print("Fly - on_exit")
