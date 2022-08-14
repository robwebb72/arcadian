class GameStateManager:
    def __init__(self) -> None:
        self._states = {}
        self._current_state = None
        self.current_state_activated = False

    def add_state(self, key: str, state):
        if key in self._states:
            raise KeyError(f"State '{key}' already added to GameStateManager")
        self._states[key] = state

    def set_state(self, key):
        new_state = self._states[key]
        self.current_state_activated = False
        self._current_state = new_state

    def get_state(self):
        return self._current_state
