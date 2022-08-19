import typing

import pygame

import colours
import utility_functions
from asteroid import AsteroidField
from gamestateinterface import GameStateInterface
from player import Player
from particle_library import ParticleExplosion


class GameWorld:
    def __init__(self, screen_size: typing.Tuple[int, int]) -> None:
        self.player = Player(screen_size)
        self.asteroids = AsteroidField(10, screen_size)

    def update(self, dt_sec: float) -> None:
        self.asteroids.update(dt_sec)
        self.player.update(dt_sec)

    def draw(self, screen: pygame.Surface) -> None:
        self.asteroids.draw(screen)
        self.player.draw(screen)

    def player_collided_with_asteroid(self) -> bool:
        return self.asteroids.check_for_collision(self.player.get_masked_surface(), self.player.position)

GAME_RUNNING = 1
GAME_OVER = 2

def create_background_pane() -> pygame.Surface:
        surface = pygame.Surface((70, 30))
        surface.fill((127, 127, 127))
        surface.set_alpha(127)
        return surface

class GameState(GameStateInterface):
    def __init__(self, system_settings):
        self._screen_size = system_settings.get_screen_size()
        self._system_settings = system_settings
        self._state: int = 0
        self._background_pane = create_background_pane()
        self._explosion_sound = pygame.mixer.Sound("sfx/player_expd.wav")

    def initialise(self):
        self._game_world = GameWorld(self._screen_size)
        self.set_state(GAME_RUNNING)

    def set_state(self, state):
        self._state = state
        if state == GAME_RUNNING:
            self._game_time = 0
        elif state == GAME_OVER:
            self._state_timer = 5
            self._game_world.player.set_player_dead()
            self._explosion = ParticleExplosion(self._game_world.player.position)
            self._explosion.turn_on()
            self._explosion_sound.play()

    def update(self, dt_sec: float) -> None:
        if self._state == GAME_OVER:
            self.update_when_game_over(dt_sec)
        if self._state == GAME_RUNNING:
            self.update_when_game_running(dt_sec)

    def update_when_game_running(self, dt_sec):
        if self._game_world.player_collided_with_asteroid():
            self.set_state(GAME_OVER)
            return
        self._game_time += dt_sec
        speed_factor = 1 + int(self._game_time / 10) / 10
        self._game_world.asteroids.set_speed_factor(speed_factor)
        if self._game_time > self._system_settings._best_time:
            self._system_settings._best_time = self._game_time
        self._game_world.update(dt_sec)

    def update_when_game_over(self, dt_sec):
        if self._state_timer > 0:
            self._state_timer -= dt_sec
        if self._state_timer <= 0:
            self._system_settings.game_state_manager.set_state("menu")
        self._game_world.asteroids.update(dt_sec)
        self._explosion.update(dt_sec)

    def handle_input(self, type: int, key: int) -> None:
        if self._state == GAME_RUNNING:
            self._game_world.player.update_from_input(key, type)
            if key == pygame.K_a and type == pygame.KEYDOWN:
                self._game_world.asteroids.set_speed_factor(2.0)
        if key == pygame.K_ESCAPE:
            self._system_settings.game_state_manager.set_state("menu")
        if key == pygame.K_0:
            self.set_state(GAME_OVER)

    def draw(self, screen: pygame.Surface) -> None:
        if self._state == GAME_RUNNING:
            self.draw_game_running(screen)
        elif self._state == GAME_OVER:
            self.draw_game_over(screen)

    def draw_game_running(self, screen):
        self._game_world.draw(screen)
        self._print_info(screen)

    def draw_game_over(self, screen):
        self._game_world.asteroids.draw(screen)
        self._explosion.draw(screen)
        screen_width = screen.get_width()
        font = self._system_settings.get_font()
        utility_functions.print(
            screen, font, "GAME OVER", screen_width * 0.5, 350, colours.WHITE
        )
        self._print_info(screen)

    def _print_info(self, screen: pygame.Surface):
        screen_width = screen.get_width()
        font = self._system_settings.get_font()

        screen.blit(self._background_pane, (220, 7))
        utility_functions.print(
            screen, font, "TIME", screen_width * 0.5, 15, colours.AQUA
        )
        gametime_str = utility_functions.create_time_str(self._game_time)
        utility_functions.print(
            screen, font, gametime_str, screen_width * 0.5, 30, colours.AQUA
        )
        screen.blit(self._background_pane, (350, 7))
        utility_functions.print(
            screen, font, "BEST TIME", screen_width * 0.75, 15, colours.AQUA
        )
        besttime_str = utility_functions.create_time_str(
            self._system_settings._best_time
        )
        utility_functions.print(
            screen, font, besttime_str, screen_width * 0.75, 30, colours.AQUA
        )
