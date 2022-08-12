import random
import typing

import pygame


class Asteroid:
    def __init__(self, screen_size: typing.Tuple[int, int], image : pygame.Surface) -> None:
        self._screen_width, self._screen_height = screen_size
        self._speed_factor = 1.0
        self._rect : pygame.Rect = pygame.Rect(0,0, 60, 60)
        self._image = image
        self._create_new()
        self.is_alive : bool = True
        self._location_y = random.randrange(-self._screen_height, -self._rect.height)

    def set_image(self, surface : pygame.Surface) -> None:
        self._image = surface
        self._rect = surface.get_rect()

    def update(self, dt_sec: float):
        if self.is_alive == False:
            return
        self._location_y += self._speed * dt_sec * self._speed_factor
        if self._location_y > self._screen_height + self._rect.height:
            self.is_alive = False
        else:
            self._position = (self._location_x, self._location_y)

    def draw(self, screen: pygame.Surface):
        screen.blit(self._image, self._position)

    def update_speed_factor(self, factor: float):
        self._speed_factor = factor

    def temp(self, position, size):
        self._position = position
        self._size = size

    def _create_new(self):
        self._speed = random.randrange(100, 200)
        self._location_x = random.randint(self._rect.width, self._screen_width - self._rect.width)
        self._location_y = -self._rect.height
        self._position = (self._location_x, self._location_y)

    def create_new(self, surface : pygame.Surface) -> None:
        self.set_image(surface)
        self._create_new()
        self.is_alive = True

class AsteroidField:
    def __init__(self, nasteroids: int, screen_size: typing.Tuple) -> None:
        self._images :typing.List[pygame.Surface]= []

        for i in range(6):
            image: pygame.Surface = pygame.image.load(f"images/asteroid{i}.png")
            self._images.append(image)

        self._screen_width, self._screen_height = screen_size
        self._speed_factor = 1.0
        self._asteroids = []
        for i in range(nasteroids):
            self._asteroids.append(Asteroid(screen_size,random.choice(self._images)))


    def update(self, dt_sec: float) -> None:
        for asteroid in self._asteroids:
            if asteroid.is_alive:
                asteroid.update(dt_sec)
            else:
                asteroid.create_new(random.choice(self._images))

    def draw(self, screen: pygame.Surface) -> None:
        [asteroid.draw(screen) for asteroid in self._asteroids]

    def set_speed_factor(self, speed_factor: float) -> None:
        self._speed_factor = speed_factor
        [asteroid.update_speed_factor(speed_factor) for asteroid in self._asteroids]
