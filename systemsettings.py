from typing import Tuple

from pygame import Surface, font, time


class SystemSettings:
    def __init__(self, screen: Surface, clock: time.Clock) -> None:
        self._screen: Surface = screen
        self._clock: time.Clock = clock
        self._font: font.Font = font.Font("freesansbold.ttf", 12)
        self._best_time: float = 0
        self.app_quit = False
        self.current_joystick = None

    def get_screen(self) -> Surface:
        return self._screen

    def get_clock(self) -> time.Clock:
        return self._clock

    def get_screen_size(self) -> Tuple[int, int]:
        width = self._screen.get_width()
        height = self._screen.get_height()
        return (width, height)

    def get_font(self) -> font.Font:
        return self._font
