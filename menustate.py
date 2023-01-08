import pygame
from pygame import Surface

import utility_functions
from colours import AQUA, GREEN
from gamestate_manager import set_current_state_active, set_state
from systemsettings import SystemSettings


class MenuState:
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

    # TODO: Write joystick code!
    def handle_joystick(self, button, axis0, axis1) -> None:
        if button:
            set_state("game")

    def draw(self, screen: Surface) -> None:
        font = self._system_settings.get_font()
        width = self._screen_width
        utility_functions.print(
            screen, font, "Welcome to Arcadian", width * 0.5, 150, GREEN
        )
        utility_functions.print(
            screen, font, "Press FIRE or SPACE to Start", width * 0.5, 500, AQUA
        )
        utility_functions.print(
            screen, font, "Press ESCAPE to Quit", width * 0.5, 530, AQUA
        )

        besttime_str = utility_functions.create_time_str(
            self._system_settings._best_time
        )
        screen.blit(self._surface, (350, 7))
        utility_functions.print(
            screen, font, "BEST TIME", self._screen_width * 0.75, 15, AQUA
        )
        utility_functions.print(
            screen, font, besttime_str, self._screen_width * 0.75, 30, AQUA
        )

    def handle_input(self, type: int, key: int) -> None:
        if key == pygame.K_ESCAPE and type == pygame.KEYDOWN:
            self._system_settings.app_quit = True
            set_current_state_active(False)
        if key == pygame.K_SPACE and type == pygame.KEYDOWN:
            set_state("game")
