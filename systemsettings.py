from typing import Tuple

from pygame import Surface, font, time

from game_state_manager import GameStateManager


class SystemSettings:
    def __init__(self, screen: Surface, clock: time.Clock) -> None:
        self._screen: Surface = screen
        self._clock: time.Clock = clock
        self._font: font.Font = font.Font("freesansbold.ttf", 12)
        #self._currentstate: str = "menu"
        #self._init_state: bool = True
        self._best_time: float = 0
        self.gamestate = GameStateManager()
        self.app_quit = False

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


    def add_state(self, key, state):
        self.gamestate.add_state(key, state)

    def get_state(self) -> str:
        return self.gamestate.get_current_state()

    def set_state(self, state: str) -> None:
        self.gamestate.set_current_state(state)
        self.set_state_is_activated(False)

    def set_state_is_activated(self, state: bool) -> None:
        self.gamestate._current_state_activated = state

    def get_state_is_activated(self) -> bool:
        return self.gamestate._current_state_activated
