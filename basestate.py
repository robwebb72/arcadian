class BaseState:
    def __init__(self, key: str) -> None:
        self._key = key
        self._state_manager = None

    def set_state_manager(self, manager) -> None:
        self._state_manager = manager
