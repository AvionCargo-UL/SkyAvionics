from src.domain.state_machine.state import State
from src.domain.state_machine.states_enum import StateEnum


class StateMachine:
    def __init__(self, states: dict[StateEnum, State], initial_state: StateEnum):
        self.__states = states

        self.__current_state = self.__get_state_by_class(initial_state)
        self.__current_state.on_enter()

    def __get_state_by_class(self, state_class: StateEnum) -> State:
        return self.__states[state_class]

    def __change_state(self, next_state: State):
        self.__current_state.on_exit()
        self.__current_state = next_state
        self.__current_state.on_enter()

    def force_transition(self, state: StateEnum):
        next_state = self.__get_state_by_class(state)
        self.__change_state(next_state)

    def execute(self):
        next_state: StateEnum = self.__current_state.execute()

        if next_state is not None and next_state != self.__current_state:
            state = self.__get_state_by_class(next_state)
            self.__change_state(state)
