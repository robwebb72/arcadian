import pygame

import colours
from basegamestate import BaseGameState
from systemsettings import SystemSettings


class MenuState(BaseGameState):
    def __init__(self, system_settings: SystemSettings) -> None:
        self._game_time: float = 0
        self._system_settings: SystemSettings = system_settings
        self._screen_width = self._system_settings._screen.get_width()
        super().__init__()

    def initialise(self) -> None:
        self._system_settings.set_init_state(False)

    def update(self, dt_sec: float) -> None:
        return super().update(dt_sec)

    def draw(self, screen: pygame.Surface) -> None:
        super().print(screen, "Welcome to Arcadian", self._screen_width *.5, 150, colours.GREEN)
        super().print(screen, "Press SPACE to Start", self._screen_width *.5, 500, colours.AQUA)
        super().print(screen, "Press ESCAPE to Quit", self._screen_width *.5, 530, colours.AQUA)

        besttime_str = super().create_time_str(self._system_settings._best_time)
        super().print(screen, "BEST TIME", self._screen_width * 0.75, 15, colours.AQUA)
        super().print(screen, besttime_str, self._screen_width * 0.75, 30, colours.AQUA)

        return super().draw(screen)

    def handle_input(self, type: int, key: int) -> None:
        if key == pygame.K_ESCAPE and type == pygame.KEYDOWN:
            self._system_settings.set_state("exit")
        if key == pygame.K_SPACE and type == pygame.KEYDOWN:
            self._system_settings.set_state("game")
        return super().handle_input(type, key)
