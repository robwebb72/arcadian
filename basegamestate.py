import pygame

# from state_manager import StateManager


class BaseGameState:
    def __init__(self, key: str) -> None:
        self._key = key
        self._state_manager = None

    def set_state_manager(self, manager):
        self._state_manager = manager

    def change_state(self, state_key: str) -> None:
        self._state_manager.set_current_state_by_key(state_key)

    def initialise(self) -> None:
        pass

    def update(self, dt_sec: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass

    def handle_input(self, type: int, key: int) -> None:
        pass
