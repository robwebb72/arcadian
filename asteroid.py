import random
import typing

import pygame
from typing import List, Tuple
from maskedsurface import MaskedSurface


class Asteroid:
    def __init__(
        self, screen_size: Tuple[int, int], maskedSurface: MaskedSurface
    ) -> None:
        self._screen_width: int = screen_size[0]
        self._screen_height: int = screen_size[1]

        self._speed_factor: float = 1.0
        self._maskedSurface: MaskedSurface = maskedSurface
        self._create_new()
        self.is_active: bool = True
        self._location_y = random.randrange(
            -self._screen_height, -self._maskedSurface.rect.height
        )

    def set_image(self, maskedSurface: MaskedSurface) -> None:
        self._maskedSurface = maskedSurface

    def update(self, dt_sec: float):
        if self.is_active == False:
            return
        self._location_y += self._speed * dt_sec * self._speed_factor
        if self._location_y > self._screen_height + self._maskedSurface.rect.height:
            self.is_active = False
        else:
            self._position = (self._location_x, self._location_y)

    def draw(self, screen: pygame.Surface):
        screen.blit(self._maskedSurface.surface, self._position)

    def update_speed_factor(self, factor: float):
        self._speed_factor = factor

    def _create_new(self):
        self._speed = random.randrange(100, 200)
        width = self._maskedSurface.rect.width
        self._location_x = random.randint(
            int(width / 2), self._screen_width - int(width / 2)
        )
        self._location_y = -self._maskedSurface.rect.height
        self._position = (self._location_x, self._location_y)

    def create_new(self, maskedSurface: MaskedSurface) -> None:
        self._maskedSurface = maskedSurface
        self._create_new()
        self.is_active = True


class AsteroidField:
    def __init__(self, nasteroids: int, screen_size: Tuple[int, int]) -> None:
        self._surfaces: List[MaskedSurface] = []
        self.load_surfaces()
        self._screen_width: int = screen_size[0]
        self._screen_height: int = screen_size[1]
        self._speed_factor: float = 1.0
        self._asteroids: List[Asteroid] = []
        for i in range(nasteroids):
            self._asteroids.append(Asteroid(screen_size, random.choice(self._surfaces)))

    def load_surfaces(self) -> None:
        for i in range(6):
            surface: pygame.Surface = pygame.image.load(f"images/asteroid{i}.png")
            maskedSurface: MaskedSurface = MaskedSurface(surface)
            self._surfaces.append(maskedSurface)

    def update(self, dt_sec: float) -> None:
        for asteroid in self._asteroids:
            if asteroid.is_active:
                asteroid.update(dt_sec)
            else:
                asteroid.create_new(random.choice(self._surfaces))

    def draw(self, screen: pygame.Surface) -> None:
        [asteroid.draw(screen) for asteroid in self._asteroids]

    def set_speed_factor(self, speed_factor: float) -> None:
        self._speed_factor = speed_factor
        [asteroid.update_speed_factor(speed_factor) for asteroid in self._asteroids]
