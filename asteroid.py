import random
from typing import List, Tuple

import pygame
from pygame import Vector2

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
        self.position.y = random.randrange(
            -self._screen_height, -self._maskedSurface.rect.height
        )


    def set_image(self, maskedSurface: MaskedSurface) -> None:
        self._maskedSurface = maskedSurface

    def update(self, dt_sec: float):
        if self.is_active == False:
            return
        self.position.y += self._speed * dt_sec * self._speed_factor
        if self.position.y > self._screen_height + self._maskedSurface.rect.height:
            self.is_active = False

    def draw(self, screen: pygame.Surface):
        screen.blit(self._maskedSurface.surface, self.position)

    def update_speed_factor(self, factor: float):
        self._speed_factor = factor

    def _create_new(self):
        self._speed = random.randrange(100, 200)
        width = self._maskedSurface.rect.width
        pos_x = random.randint(
            int(width / 2), self._screen_width - int(width / 2)
        )
        pos_y = -self._maskedSurface.rect.height
        self.position: Vector2 = Vector2(pos_x, pos_y)

    def create_new(self, maskedSurface: MaskedSurface) -> None:
        self._maskedSurface = maskedSurface
        self._create_new()
        self.is_active = True

    def collide_with(self, maskedSurface : MaskedSurface, position: Vector2) -> bool:
        this_rect = self._maskedSurface.rect
        other_rect= maskedSurface.rect
        this_rect.x = self.position.x
        this_rect.y = self.position.y

        other_rect.x = position.x
        other_rect.y = position.y

        if other_rect.colliderect(this_rect) == False:
            return False

        collideswith = maskedSurface.mask.overlap(self._maskedSurface.mask, self.position - position) != None
        return collideswith

class AsteroidField:
    def __init__(self, nasteroids: int, screen_size: Tuple[int, int]) -> None:
        self._surfaces: List[MaskedSurface] = []
        self.load_surfaces()
        self._screen_width: int = screen_size[0]
        self._screen_height: int = screen_size[1]
        self._speed_factor: float = 1.0
        self._asteroids: List[Asteroid] = []
        for i in range(nasteroids):
            asteroid = Asteroid(screen_size, random.choice(self._surfaces))
            self._asteroids.append(asteroid)

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

    def check_for_collision(self, maskedSurface: MaskedSurface, position: Vector2) -> bool:
        for asteroid in self._asteroids:
            if asteroid.collide_with(maskedSurface, position):
                return True
        return False
