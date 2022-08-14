from typing import Dict

from basegamestate import BaseGameState


class StateManager:
    def __init__(self) -> None:
        self._states: Dict[str, BaseGameState] = {}
        self._current_state: BaseGameState = None

    def add_state(self, state: BaseGameState):
        if state._key in self._states:
            raise KeyError
        self._states[state._key] = state
        state.set_state_manager(self)

    def get_current_state(self) -> BaseGameState:
        return self._current_state

    def set_current_state_by_key(self, new_state: str) -> None:
        # May throw KeyError - might need to handle this?
        self._current_state = self._states[new_state]

    def set_current_state_by_state(self, state: BaseGameState) -> None:
        # May throw KeyError - might need to handle this?
        self._current_state = self._states[state._key]
