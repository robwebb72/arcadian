import random
import typing
import pygame
import colours


class Asteroid:
    def __init__(self, screen_size: typing.Tuple[int, int]) -> None:
        self._screen_width, self._screen_height = screen_size
        self._speed_factor = 1.0
        self._create_new()
        self._location_y = random.randrange(-self._screen_height, -self._size)

    def update(self, dt_sec: float):
        self._location_y += self._speed * dt_sec * self._speed_factor
        if self._location_y > self._screen_height + self._size:
            self._create_new()
        self._position = (self._location_x, self._location_y)

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, colours.BLACK, self._position, self._size + 2)
        pygame.draw.circle(screen, colours.GRAY, self._position, self._size)
        offset_x = (int)(self._position[0] - self._size * 0.15)
        offset_y = (int)(self._position[1] - self._size * 0.15)
        pygame.draw.circle(
            screen, colours.WHITE, (offset_x, offset_y), self._size * 0.6
        )

    def update_speed_factor(self, factor: float):
        self._speed_factor = factor

    def temp(self, position, size):
        self._position = position
        self._size = size

    def _create_new(self):
        self._size = random.randint(10, 70)
        self._speed = random.randrange(100, 200)
        self._location_x = random.randint(self._size, self._screen_width - self._size)
        self._location_y = -self._size
        self._position = (self._location_x, self._location_y)


class AsteroidField:
    def __init__(self, nasteroids: int, screen_size: typing.Tuple) -> None:
        self._screen_width, self._screen_height = screen_size
        self._speed_factor = 1.0
        self._asteroids = []
        for i in range(nasteroids):
            self._asteroids.append(Asteroid(screen_size))

    def update(self, dt_sec: float) -> None:
        [asteroid.update(dt_sec) for asteroid in self._asteroids]

    def draw(self, screen: pygame.Surface) -> None:
        [asteroid.draw(screen) for asteroid in self._asteroids]

    def set_speed_factor(self, speed_factor: float) -> None:
        self._speed_factor = speed_factor
        [asteroid.update_speed_factor(speed_factor) for asteroid in self._asteroids]
