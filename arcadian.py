import pygame
import sys
import colours
import typing

from player import Player
from starfield import Starfield
from asteroid import AsteroidField

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 768
FPS = 30


class SystemSettings:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self._screen: pygame.Surface = screen
        self._clock: pygame.time.Clock = clock

    def get_screen(self):
        return self._screen

    def get_clock(self):
        return self._clock

    def get_screen_size(self):
        width = self._screen.get_width()
        height = self._screen.get_height()
        return (width, height)


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


def game_loop_init(settings: SystemSettings) -> GameData:
    game_data = GameData(settings.get_screen_size())
    return game_data


def game_loop(settings: SystemSettings):

    game_time: float = 0
    screen = settings.get_screen()
    clock = settings.get_clock()

    fontObj = pygame.font.Font("freesansbold.ttf", 12)
    textSurfaceObj = fontObj.render("Welcome to Arcadian", True, colours.GREEN)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (SCREEN_WIDTH / 2, 150)

    game_data = game_loop_init(settings)
    starfield = Starfield(200, (SCREEN_WIDTH, SCREEN_HEIGHT))

    game_exit = False
    while not game_exit:
        dt_sec = clock.tick(FPS) / 1000
        game_time += dt_sec

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if hasattr(event, "key"):
                game_data.player.update_from_input(event.key, event.type)
                if event.key == pygame.K_a and event.type == pygame.KEYDOWN:
                    game_data.asteroids.set_speed_factor(2.0)
                if event.key == pygame.K_ESCAPE:
                    game_exit = True

        starfield.update(dt_sec)
        game_data.update(dt_sec)

        milliseconds_string = f"{int(game_time * 10)% 10}"
        seconds_string = f"{(int(game_time) % 60):0>2}"
        minutes_string = f"{(int(game_time / 60) % 60):0>2}"
        hours_string = f"{(int(game_time / 3600)):0>2}"

        game_time_string = f'{hours_string}:{minutes_string}:{seconds_string}.{milliseconds_string}'
        game_time_SurfaceObj = fontObj.render(game_time_string, True, colours.AQUA)
        game_time_RectObj = game_time_SurfaceObj.get_rect()
        game_time_RectObj.center = (SCREEN_WIDTH / 2, 20)

        screen.fill(colours.BLACK)
        starfield.draw(screen)
        game_data.draw(screen)
        screen.blit(textSurfaceObj, textRectObj)
        screen.blit(game_time_SurfaceObj, game_time_RectObj)

        pygame.display.update()


def game_init() -> SystemSettings:
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Arcadian")
    return SystemSettings(screen, clock)


def game():
    settings = game_init()
    game_loop(settings)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game()
