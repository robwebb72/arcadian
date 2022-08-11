import pygame

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 768
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_RECT = pygame.Rect(0,0,PLAYER_WIDTH, PLAYER_HEIGHT)


class Player:
    def __init__(self):
        self._direction_left = False
        self._direction_right = False
        self._direction_up = False
        self._direction_down = False
        self.location_x = (SCREEN_WIDTH - PLAYER_WIDTH) / 2
        self.location_y = 708
        self.speed = 200
        image = pygame.image.load("images/player.png")

        self._image_straight = self._get_image_at(image, PLAYER_RECT)
        self._image_left = self._get_image_at(image, pygame.Rect(PLAYER_WIDTH, 0, PLAYER_WIDTH, PLAYER_HEIGHT))
        self._image_right = self._get_image_at(image, pygame.Rect(PLAYER_WIDTH*2, 0, PLAYER_WIDTH, PLAYER_HEIGHT))

    def _get_image_at(self, surface, rect: pygame.Rect) -> pygame.Surface:
        new_surface = pygame.Surface(rect.size)
        new_surface.blit(surface, (0,0), rect)
        return new_surface


    def update(self, dt_sec):
        if self._direction_left:
            self.location_x -= dt_sec * self.speed
        if self._direction_right:
            self.location_x += dt_sec * self.speed
        if self._direction_up:
            self.location_y -= dt_sec * self.speed
        if self._direction_down:
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
