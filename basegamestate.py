import pygame
import typing


class BaseGameState:
    def state_init(self):
        pass

    def initialise(self) -> None:
        pass

    def update(self, dt_sec: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass

    def handle_input(self, type: int, key: int) -> None:
        pass


