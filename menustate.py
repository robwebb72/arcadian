import pygame
from pygame import Surface

import colours
import utility_functions
from systemsettings import SystemSettings


class MenuState():
    def __init__(self, system_settings: SystemSettings) -> None:
        self._game_time: float = 0
        self._system_settings: SystemSettings = system_settings
        self._screen_width = self._system_settings._screen.get_width()
        self._surface = pygame.Surface((70, 30))
        self._surface.fill((127, 127, 127))
        self._surface.set_alpha(127)

    def initialise(self) -> None:
        pass

    def update(self, dt_sec: float) -> None:
        pass

    def draw(self, screen: Surface) -> None:
        font = self._system_settings.get_font()
        screen_width = self._screen_width
        utility_functions.print(
            screen, font, "Welcome to Arcadian", screen_width * 0.5, 150, colours.GREEN
        )
        utility_functions.print(
            screen, font, "Press SPACE to Start", screen_width * 0.5, 500, colours.AQUA
        )
        utility_functions.print(
            screen, font, "Press ESCAPE to Quit", screen_width * 0.5, 530, colours.AQUA
        )

        besttime_str = utility_functions.create_time_str(
            self._system_settings._best_time
        )
        screen.blit(self._surface, (350, 7))
        utility_functions.print(
            screen, font, "BEST TIME", self._screen_width * 0.75, 15, colours.AQUA
        )
        utility_functions.print(
            screen, font, besttime_str, self._screen_width * 0.75, 30, colours.AQUA
        )

    def handle_input(self, type: int, key: int) -> None:
        if key == pygame.K_ESCAPE and type == pygame.KEYDOWN:
            self._system_settings.app_quit = True
            self._system_settings.game_state_manager.current_state_activated = False
        if key == pygame.K_SPACE and type == pygame.KEYDOWN:
            self._system_settings.game_state_manager.set_state("game")
