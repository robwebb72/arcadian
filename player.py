import pygame

import colours
from typing import Tuple, List
from maskedsurface import MaskedSurface
from particle_library import ParticleJetPlume

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_RECT = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)


class Player:
    def __init__(self, screen_size: Tuple[int, int]) -> None:
        self._direction_left: bool = False
        self._direction_right: bool = False
        self._direction_up: bool = False
        self._direction_down: bool = False
        self._screen_width, self._screen_height = screen_size
        pos_x: float = (self._screen_width - PLAYER_WIDTH) / 2
        self.position: pygame.math.Vector2 = pygame.math.Vector2(pos_x, 708)
        self._speed: float = 200
        self._frames: List[MaskedSurface] = []
        self._load_frames()
        self._frame_number: int = 0
        self._alive = True

        self._jet_left = ParticleJetPlume(self._jet_left_position())
        self._jet_right = ParticleJetPlume(self._jet_right_position())
        self._jet_left.turn_on()
        self._jet_right.turn_on()

    def _update_jet_plume_positions(self):
        self._jet_left.update_position(self._jet_left_position())
        self._jet_right.update_position(self._jet_right_position())

    def _jet_left_position(self):
        return self.position + pygame.math.Vector2(11, 30)

    def _jet_right_position(self):
        return self.position + pygame.math.Vector2(17, 30)

    def _load_frames(self) -> None:
        image = pygame.image.load("images/player.png").convert()
        image_straight = self._get_image_at(image, PLAYER_RECT)
        image_left = self._get_image_at(
            image, pygame.Rect(PLAYER_WIDTH, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        )
        image_right: pygame.Surface = self._get_image_at(
            image,
            pygame.Rect(PLAYER_WIDTH * 2, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        )
        self._frames.append(MaskedSurface(image_straight))
        self._frames.append(MaskedSurface(image_left))
        self._frames.append(MaskedSurface(image_right))

    def _get_image_at(
        self, surface: pygame.Surface, rect: pygame.Rect
    ) -> pygame.Surface:
        new_surface: pygame.Surface = pygame.Surface(rect.size)
        new_surface.set_colorkey(colours.BLACK)
        new_surface.blit(surface, (0, 0), rect)
        return new_surface

    def update(self, dt_sec: float) -> None:
        if self._alive:
            delta_vec: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
            if self._direction_left:
                delta_vec.x -= dt_sec * self._speed
            if self._direction_right:
                delta_vec.x += dt_sec * self._speed
            if self._direction_up:
                delta_vec.y -= dt_sec * self._speed
            if self._direction_down:
                delta_vec.y += dt_sec * self._speed
            self.position += delta_vec
            self._check_bounds()
            self._update_jet_plume_positions()
            self._jet_left.update(dt_sec)
            self._jet_right.update(dt_sec)

    def set_player_dead(self):
        self._alive = False

    def _check_bounds(self) -> None:
        if self.position.y < self._screen_height / 2:
            self.position.y = self._screen_height / 2
        if self.position.x < 5:
            self.position.x = 5
        if self.position.y > self._screen_height - 35:
            self.position.y = self._screen_height - 35
        if self.position.x > self._screen_width - 35:
            self.position.x = self._screen_width - 35

    def update_from_input(self, key: int, event_type: int) -> None:
        if self._alive is False:
            return
        if key == pygame.K_LEFT:
            self._direction_left = event_type == pygame.KEYDOWN
        elif key == pygame.K_RIGHT:
            self._direction_right = event_type == pygame.KEYDOWN
        elif key == pygame.K_UP:
            self._direction_up = event_type == pygame.KEYDOWN
        elif key == pygame.K_DOWN:
            self._direction_down = event_type == pygame.KEYDOWN
        self._update_frame_number()

    def _update_frame_number(self):
        self._frame_number = 0
        if self._direction_left and not self._direction_right:
            self._frame_number = 1
        elif self._direction_right and not self._direction_left:
            self._frame_number = 2

    def get_masked_surface(self) -> MaskedSurface:
        return self._frames[self._frame_number]

    def draw(self, screen):
        if self._alive:
            surface = self.get_masked_surface().surface
            screen.blit(surface, self.position)
            self._jet_left.draw(screen)
            self._jet_right.draw(screen)
