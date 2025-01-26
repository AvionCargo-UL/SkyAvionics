from src.domain.state_machine.state import State
from src.domain.state_machine.states_enum import StateEnum


class DetectAruco(State):
    def on_enter(self):
        print("DetectAruco - on_enter")

    def execute(self) -> StateEnum:
        print("DetectAruco - execute")
        return StateEnum.IDLE

    def on_exit(self):
        print("DetectAruco - on_exit")
