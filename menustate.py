import pygame

import colours
from basegamestate import BaseGameState
from systemsettings import SystemSettings


class MenuState(BaseGameState):
    def __init__(self, system_settings: SystemSettings) -> None:
        self._game_time: float = 0
        self._system_settings: SystemSettings = system_settings
        self._textSurfaceObj = self._system_settings.get_font().render(
            "Welcome to Arcadian", True, colours.GREEN
        )
        self._textRectObj = self._textSurfaceObj.get_rect()
        super().__init__()

    def initialise(self) -> None:
        self._textRectObj.center = (self._system_settings.get_screen_size()[0] / 2, 150)
        self._system_settings.set_init_state(False)

    def update(self, dt_sec: float) -> None:
        return super().update(dt_sec)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._textSurfaceObj, self._textRectObj)
        return super().draw(screen)

    def handle_input(self, type: int, key: int) -> None:
        if key == pygame.K_ESCAPE and type == pygame.KEYDOWN:
            self._system_settings.set_state("exit")
        if key == pygame.K_SPACE and type == pygame.KEYDOWN:
            self._system_settings.set_state("game")
        return super().handle_input(type, key)
