import typing

import pygame

import colours
from asteroid import AsteroidField
from basegamestate import BaseGameState
from player import Player
from systemsettings import SystemSettings


class GameData:
    def __init__(self, screen_size: typing.Tuple[int, int]) -> None:
        self.player = Player()
        self.asteroids = AsteroidField(10, screen_size)

    def update(self, dt_sec: float) -> None:
        self.player.update(dt_sec)
        self.asteroids.update(dt_sec)

    def draw(self, screen: pygame.Surface) -> None:
        self.asteroids.draw(screen)
        self.player.draw(screen)


class GameState(BaseGameState):
    def __init__(self, system_settings: SystemSettings) -> None:
        self._game_time: float = 0
        self._system_settings: SystemSettings = system_settings
        super().__init__()

    def initialise(self):
        self._game_time = 0
        self._game_data = GameData(self._system_settings.get_screen_size())
        self._system_settings.set_init_state(False)

    def update(self, dt_sec: float) -> None:
        self._game_time += dt_sec
        speed_factor = 1 + int(self._game_time / 10) / 10
        self._game_data.asteroids.set_speed_factor(speed_factor)
        if self._game_time > self._system_settings._best_time:
            self._system_settings._best_time = self._game_time
        self._game_data.update(dt_sec)
        return super().update(dt_sec)

    def handle_input(self, type: int, key: int) -> None:
        self._game_data.player.update_from_input(key, type)
        if key == pygame.K_a and type == pygame.KEYDOWN:
            self._game_data.asteroids.set_speed_factor(2.0)
        if key == pygame.K_ESCAPE:
            self._system_settings.set_state("menu")

    def print_to_screen(
        self,
        screen: pygame.Surface,
        message: str,
        x: int,
        y: int,
        colour: typing.Tuple[int, int, int],
    ) -> None:
        print_surface = self._system_settings.get_font().render(message, True, colour)
        print_rect = print_surface.get_rect()
        print_rect.center = (x, y)
        screen.blit(print_surface, print_rect)

    def create_time_str(self, time: float) -> str:
        milliseconds_string = f"{int(time * 10)% 10}"
        seconds_string = f"{(int(time) % 60):0>2}"
        minutes_string = f"{(int(time / 60) % 60):0>2}"
        hours_string = f"{(int(time / 3600)):0>2}"
        return f"{hours_string}:{minutes_string}:{seconds_string}.{milliseconds_string}"

    def draw(self, screen: pygame.Surface) -> None:
        self._game_data.draw(screen)
        gametime_str = self.create_time_str(self._game_time)
        besttime_str = self.create_time_str(self._system_settings._best_time)
        screen_width = self._system_settings.get_screen_size()[0]
        speed_str = f"x {self._game_data.asteroids._speed_factor:.2}"
        self.print_to_screen(screen, speed_str, screen_width * 0.25, 30, colours.AQUA)

        self.print_to_screen(screen, "TIME", screen_width * 0.5, 15, colours.AQUA)
        self.print_to_screen(screen, gametime_str, screen_width * 0.5, 30, colours.AQUA)
        self.print_to_screen(screen, "BEST TIME", screen_width * 0.75, 15, colours.AQUA)
        self.print_to_screen(
            screen, besttime_str, screen_width * 0.75, 30, colours.AQUA
        )
        return super().draw(screen)
