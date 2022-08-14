import typing
from ctypes import util

import pygame

import colours
import utility_functions
from asteroid import AsteroidField
from basegamestate import BaseGameState
from gamestateinterface import GameStateInterface
from player import Player
from systemsettings import SystemSettings


class GameData:
    def __init__(self, screen_size: typing.Tuple[int, int]) -> None:
        self.player = Player()
        self.asteroids = AsteroidField(10, screen_size)
        self.player_is_alive = True

    def update(self, dt_sec: float) -> None:
        self.asteroids.update(dt_sec)
        if self.player_is_alive:
            self.player.update(dt_sec)

    def draw(self, screen: pygame.Surface) -> None:
        self.asteroids.draw(screen)
        self.player.draw(screen)


GAME_RUNNING = 1
GAME_OVER = 2


class GameState(GameStateInterface):
    def __init__(self, system_settings: SystemSettings) -> None:
        self._game_time: float = 0
        self.boom = False
        self._system_settings: SystemSettings = system_settings
        self._state: int = 0

    def initialise(self):
        self._game_time = 0
        self._game_data = GameData(self._system_settings.get_screen_size())
        self._state = GAME_RUNNING

    def update(self, dt_sec: float) -> None:
        if self._game_data.asteroids.check_for_collision(
            self._game_data.player.get_masked_surface(), self._game_data.player.position
        ):
            # self._game_data.player_is_alive = False    # commented out to test collision detection
            self.boom = True
        #        else:   # commented out to test collision detection
        self._game_time += dt_sec
        speed_factor = 1 + int(self._game_time / 10) / 10
        self._game_data.asteroids.set_speed_factor(speed_factor)
        if self._game_time > self._system_settings._best_time:
            self._system_settings._best_time = self._game_time
        self._game_data.update(dt_sec)

    def handle_input(self, type: int, key: int) -> None:
        if self._game_data.player_is_alive:
            self._game_data.player.update_from_input(key, type)
            if key == pygame.K_a and type == pygame.KEYDOWN:
                self._game_data.asteroids.set_speed_factor(2.0)
        if key == pygame.K_ESCAPE:
            self._system_settings.set_state("menu")

    def draw(self, screen: pygame.Surface) -> None:
        self._game_data.draw(screen)
        self._print_info(screen)

    def _print_info(self, screen: pygame.Surface):
        screen_width = screen.get_width()
        font = self._system_settings.get_font()

        speed_str = f"x {self._game_data.asteroids._speed_factor:.2}"
        utility_functions.print(
            screen, font, speed_str, screen_width * 0.25, 30, colours.AQUA
        )

        utility_functions.print(
            screen, font, "TIME", screen_width * 0.5, 15, colours.AQUA
        )
        gametime_str = utility_functions.create_time_str(self._game_time)
        utility_functions.print(
            screen, font, gametime_str, screen_width * 0.5, 30, colours.AQUA
        )

        utility_functions.print(
            screen, font, "BEST TIME", screen_width * 0.75, 15, colours.AQUA
        )
        besttime_str = utility_functions.create_time_str(
            self._system_settings._best_time
        )
        utility_functions.print(
            screen, font, besttime_str, screen_width * 0.75, 30, colours.AQUA
        )

        if self.boom:
            utility_functions.print(
                screen, font, "BOOOOM!!!", screen_width * 0.5, 300, colours.RED
            )
            self.boom = False
        else:
            utility_functions.print(
                screen, font, "Alive!", screen_width * 0.5, 300, colours.GREEN
            )
