import pygame

import colours
from basegamestate import BaseGameState
from systemsettings import SystemSettings


class MenuState(BaseGameState):
    def __init__(self, system_settings: SystemSettings) -> None:
        self._game_time: float = 0
        self._system_settings: SystemSettings = system_settings
        self._text_surface1 = self._system_settings.get_font().render(
            "Welcome to Arcadian", True, colours.GREEN
        )
        self._text_rect1 = self._text_surface1.get_rect()
        self._text_rect1.center = (self._system_settings.get_screen_size()[0] / 2, 150)

        self._text_surface2 = self._system_settings.get_font().render(
            "Press SPACE to Start", True, colours.AQUA
        )
        self._text_rect2 = self._text_surface2.get_rect()
        self._text_rect2.center = (self._system_settings.get_screen_size()[0] / 2, 500)

        self._text_surface3 = self._system_settings.get_font().render(
            "Press ESCAPE to Quit", True, colours.AQUA
        )
        self._text_rect3 = self._text_surface3.get_rect()
        self._text_rect3.center = (self._system_settings.get_screen_size()[0] / 2, 530)
        super().__init__()

    def initialise(self) -> None:
        self._system_settings.set_init_state(False)

    def update(self, dt_sec: float) -> None:
        return super().update(dt_sec)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._text_surface1, self._text_rect1)
        screen.blit(self._text_surface2, self._text_rect2)
        screen.blit(self._text_surface3, self._text_rect3)
        return super().draw(screen)

    def handle_input(self, type: int, key: int) -> None:
        if key == pygame.K_ESCAPE and type == pygame.KEYDOWN:
            self._system_settings.set_state("exit")
        if key == pygame.K_SPACE and type == pygame.KEYDOWN:
            self._system_settings.set_state("game")
        return super().handle_input(type, key)
