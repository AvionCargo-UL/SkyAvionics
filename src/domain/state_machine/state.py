from abc import abstractmethod, ABC

from src.domain.state_machine.states_enum import StateEnum


class State(ABC):
    @abstractmethod
    def on_enter(self):
        pass

    @abstractmethod
    def execute(self) -> StateEnum:
        pass

    @abstractmethod
    def on_exit(self):
        pass
