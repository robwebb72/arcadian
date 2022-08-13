import pygame


class MaskedSurface:
    def __init__(self) -> None:
        self.surface: pygame.Surface = None
        self.mask: pygame.Mask = None
        self.rect: pygame.Rect = None

    def __init__(self, surface: pygame.Surface) -> None:
        self.surface: pygame.Surface = surface
        self.initialise()

    def load(self, filename: str) -> None:
        self.surface.pygame.image.load(filename)
        self._initialise()

    def from_surface(self, surface: pygame.Surface) -> None:
        self.surface = surface
        self._initialise()

    def initialise(self) -> None:
        self.mask = pygame.mask.from_surface(self.surface)
        self.rect = self.surface.get_rect()
