import random

from src.domain.state_machine.state import State
from src.domain.state_machine.states_enum import StateEnum


class Takeoff(State):

    def __init__(self):
        self.__altitude = 0

    def on_enter(self):
        self.__altitude = 0
        print("Takeoff - on_enter")

    def execute(self) -> StateEnum:
        self.__altitude += random.randint(0, 10)
        print("Takeoff - execute - altitude: {0}".format(self.__altitude))
        if self.__altitude > 45:
            return StateEnum.FLY

    def on_exit(self):
        print("Takeoff - on_exit")
