import random
import typing

import pygame
from maskedsurface import MaskedSurface

class Asteroid:
    def __init__(
        self, screen_size: typing.Tuple[int, int], maskedSurface: MaskedSurface
    ) -> None:
        self._screen_width:int = screen_size[0]
        self._screen_height:int = screen_size[1]

        self._speed_factor: float = 1.0
        self._maskedSurface: MaskedSurface= maskedSurface
        self._create_new()
        self.is_alive: bool = True
        self._location_y = random.randrange(-self._screen_height, -self._maskedSurface.rect.height)

    def set_image(self, maskedSurface: MaskedSurface) -> None:
        self._maskedSurface = maskedSurface

    def update(self, dt_sec: float):
        if self.is_alive == False:
            return
        self._location_y += self._speed * dt_sec * self._speed_factor
        if self._location_y > self._screen_height + self._maskedSurface.rect.height:
            self.is_alive = False
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
            int(width/2), self._screen_width - int(width/2)
        )
        self._location_y = -self._maskedSurface.rect.height
        self._position = (self._location_x, self._location_y)

    def create_new(self, maskedSurface: MaskedSurface) -> None:
        self._maskedSurface = maskedSurface
        self._create_new()
        self.is_alive = True


class AsteroidField:
    def __init__(self, nasteroids: int, screen_size: typing.Tuple) -> None:
        self._surfaces: typing.List[MaskedSurface] = []

        for i in range(6):
            surface: pygame.Surface = pygame.image.load(f"images/asteroid{i}.png");
            maskedSurface: MaskedSurface = MaskedSurface(surface);
            self._surfaces.append(maskedSurface)

        self._screen_width, self._screen_height = screen_size
        self._speed_factor = 1.0
        self._asteroids = []
        for i in range(nasteroids):
            self._asteroids.append(Asteroid(screen_size, random.choice(self._surfaces)))

    def update(self, dt_sec: float) -> None:
        for asteroid in self._asteroids:
            if asteroid.is_alive:
                asteroid.update(dt_sec)
            else:
                asteroid.create_new(random.choice(self._surfaces))

    def draw(self, screen: pygame.Surface) -> None:
        [asteroid.draw(screen) for asteroid in self._asteroids]

    def set_speed_factor(self, speed_factor: float) -> None:
        self._speed_factor = speed_factor
        [asteroid.update_speed_factor(speed_factor) for asteroid in self._asteroids]
