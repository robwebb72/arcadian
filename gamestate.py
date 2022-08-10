import pygame
from systemsettings import SystemSettings
import colours

from basegamestate import BaseGameState
from player import Player
import typing
from asteroid import AsteroidField


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
        self._game_data.update(dt_sec)
        return super().update(dt_sec)

    def create_time_str(self) -> str:

        milliseconds_string = f"{int(self._game_time * 10)% 10}"
        seconds_string = f"{(int(self._game_time) % 60):0>2}"
        minutes_string = f"{(int(self._game_time / 60) % 60):0>2}"
        hours_string = f"{(int(self._game_time / 3600)):0>2}"
        return f"{hours_string}:{minutes_string}:{seconds_string}.{milliseconds_string}"

    def handle_input(self, type: int, key: int) -> None:
        self._game_data.player.update_from_input(key, type)
        if key == pygame.K_a and type == pygame.KEYDOWN:
            self._game_data.asteroids.set_speed_factor(2.0)
        if key == pygame.K_ESCAPE:
            self._system_settings.set_state("menu")

    def draw(self, screen: pygame.Surface) -> None:

        gametime_str = self.create_time_str()
        gametime_surface = self._system_settings.get_font().render(
            gametime_str, True, colours.AQUA
        )
        gametime_rect = gametime_surface.get_rect()
        gametime_rect.center = (self._system_settings.get_screen_size()[0] / 2, 20)

        self._game_data.draw(screen)
        #        screen.blit(textSurfaceObj, textRectObj)
        screen.blit(gametime_surface, gametime_rect)
        return super().draw(screen)
