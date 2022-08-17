import random
import typing

import pygame


class Star:
    def __init__(self, screen_size: typing.Tuple[int, int], surface: pygame.Surface):
        self._width, self._height = screen_size
        self._x: int = random.randint(0, self._width)
        self._y: float = random.randrange(self._height)
        self._rect = pygame.Rect(0, 0, 1, 1)
        self._speed: float = 0
        self._setspeed()

    def _setspeed(self) -> float:
        rand_val = random.randint(3, 7)
        self._speed = self._height / rand_val
        if rand_val < 5:
            self._rect = pygame.Rect(0, 0, 2, 2)
        else:
            self._rect = pygame.Rect(0, 0, 1, 1)

    def update(self, dt_sec: float):
        self._y += self._speed * dt_sec
        if self._y > self._height:
            self._x = random.randint(0, self._width)
            self._y = 0
            self._setspeed()

    def get_position(self):
        return (self._x, int(self._y))


class Starfield:
    def __init__(self, nstars: int, screen_size: typing.Tuple[int, int]):
        self._stars = []
        self._surface = pygame.Surface((2, 2))
        self._surface.fill((255, 255, 255))
        for i in range(nstars):
            self._stars.append(Star(screen_size, self._surface))

    def update(self, dt_sec):
        [star.update(dt_sec) for star in self._stars]

    def draw(self, screen):
        blit_list = self._create_blit_list()
        screen.blits(blit_list)

    def _create_blit_list(self):
        blit_list = []
        [
            blit_list.append((self._surface, star.get_position(), star._rect))
            for star in self._stars
        ]
        return blit_list
