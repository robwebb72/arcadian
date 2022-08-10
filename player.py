import pygame

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 768
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30


class Player:
    def __init__(self):
        self.direction_left = False
        self.direction_right = False
        self.direction_up = False
        self.direction_down = False
        self.direction = 0
        self.location_x = (SCREEN_WIDTH - PLAYER_WIDTH) / 2
        self.location_y = 708
        self.speed = 200
        self.image = pygame.image.load("images/player.png")

    def update(self, dt_sec):
        self.direction = 0
        if self.direction_left:
            self.direction = 1
            self.location_x -= dt_sec * self.speed
        if self.direction_right:
            self.direction = 2
            self.location_x += dt_sec * self.speed
        if self.direction_up:
            self.location_y -= dt_sec * self.speed
        if self.direction_down:
            self.location_y += dt_sec * self.speed
        self._check_bounds()

    def _check_bounds(self) -> None:
        if self.location_y < SCREEN_HEIGHT / 2:
            self.location_y = SCREEN_HEIGHT / 2
        if self.location_x < 5:
            self.location_x = 5
        if self.location_y > SCREEN_HEIGHT - 35:
            self.location_y = SCREEN_HEIGHT - 35
        if self.location_x > SCREEN_WIDTH - 35:
            self.location_x = SCREEN_WIDTH - 35

    def location(self):
        return (self.location_x, self.location_y)

    def rect(self):
        return pygame.Rect(
            self.direction * PLAYER_WIDTH, 0, PLAYER_WIDTH, PLAYER_HEIGHT
        )

    def right(self, state):
        self.direction_right = state

    def left(self, state):
        self.direction_left = state

    def up(self, state):
        self.direction_up = state

    def down(self, state):
        self.direction_down = state

    def draw(self, screen):
        screen.blit(self.image, self.location(), self.rect())

    def update_from_input(self, key: int, event_type: int) -> None:
        if key == pygame.K_RIGHT:
            self.right(event_type == pygame.KEYDOWN)
        elif key == pygame.K_LEFT:
            self.left(event_type == pygame.KEYDOWN)
        elif key == pygame.K_UP:
            self.up(event_type == pygame.KEYDOWN)
        elif key == pygame.K_DOWN:
            self.down(event_type == pygame.KEYDOWN)
