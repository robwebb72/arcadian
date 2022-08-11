import pygame
import typing

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 768
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_RECT = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)


class Player:
    def __init__(self) -> None:
        self._direction_left: bool = False
        self._direction_right: bool = False
        self._direction_up: bool = False
        self._direction_down: bool = False
        self._location_x: float = (SCREEN_WIDTH - PLAYER_WIDTH) / 2
        self._location_y: float = 708
        self._speed: float = 200
        image: pygame.Surface = pygame.image.load("images/player.png")

        self._image_straight: pygame.Surface = self._get_image_at(image, PLAYER_RECT)
        self._image_left: pygame.Surface = self._get_image_at(
            image, pygame.Rect(PLAYER_WIDTH, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        )
        self._image_right: pygame.Surface = self._get_image_at(
            image, pygame.Rect(PLAYER_WIDTH * 2, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        )

    def _get_image_at(
        self, surface: pygame.Surface, rect: pygame.Rect
    ) -> pygame.Surface:
        new_surface: pygame.Surface = pygame.Surface(rect.size)
        new_surface.blit(surface, (0, 0), rect)
        return new_surface

    def update(self, dt_sec: float) -> None:
        if self._direction_left:
            self._location_x -= dt_sec * self._speed
        if self._direction_right:
            self._location_x += dt_sec * self._speed
        if self._direction_up:
            self._location_y -= dt_sec * self._speed
        if self._direction_down:
            self._location_y += dt_sec * self._speed
        self._check_bounds()

    def _check_bounds(self) -> None:
        if self._location_y < SCREEN_HEIGHT / 2:
            self._location_y = SCREEN_HEIGHT / 2
        if self._location_x < 5:
            self._location_x = 5
        if self._location_y > SCREEN_HEIGHT - 35:
            self._location_y = SCREEN_HEIGHT - 35
        if self._location_x > SCREEN_WIDTH - 35:
            self._location_x = SCREEN_WIDTH - 35

    def location(self) -> typing.Tuple[float, float]:
        return (self._location_x, self._location_y)

    def draw(self, screen):
        image = self._image_straight
        if self._direction_right:
            image = self._image_right
        elif self._direction_left:
            image = self._image_left

        screen.blit(image, self.location())

    def update_from_input(self, key: int, event_type: int) -> None:
        if key == pygame.K_RIGHT:
            self._direction_right = event_type == pygame.KEYDOWN
        elif key == pygame.K_LEFT:
            self._direction_left = event_type == pygame.KEYDOWN
        elif key == pygame.K_UP:
            self._direction_up = event_type == pygame.KEYDOWN
        elif key == pygame.K_DOWN:
            self._direction_down = event_type == pygame.KEYDOWN
