from src.domain.state_machine.state import State
from src.domain.state_machine.states_enum import StateEnum


class Idle(State):
    def on_enter(self):
        print("Idle - on_enter")

    def execute(self) -> StateEnum:
        print("Idle - execute")
        return StateEnum.TAKEOFF

    def on_exit(self):
        print("Idle - on_exit")
