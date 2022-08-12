import typing

import pygame


class SystemSettings:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock) -> None:
        self._screen: pygame.Surface = screen
        self._clock: pygame.time.Clock = clock
        self._font: pygame.font.Font = pygame.font.Font("freesansbold.ttf", 12)
        self._currentstate: str = "menu"
        self._init_state: bool = True
        self._best_time: float = 0

    def get_screen(self) -> pygame.Surface:
        return self._screen

    def get_clock(self) -> pygame.time.Clock:
        return self._clock

    def get_screen_size(self) -> typing.Tuple[int, int]:
        width = self._screen.get_width()
        height = self._screen.get_height()
        return (width, height)

    def get_font(self) -> pygame.font.Font:
        return self._font

    def get_state(self) -> str:
        return self._currentstate

    def get_init_state(self) -> bool:
        return self._init_state

    def set_state(self, state: str) -> None:
        self._init_state = state != self._currentstate
        self._currentstate = state

    def set_init_state(self, state: bool) -> None:
        self._init_state = state
