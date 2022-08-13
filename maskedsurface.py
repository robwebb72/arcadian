import pygame


class MaskedSurface:
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface: pygame.Surface = surface
        self.mask: pygame.mask.Mask = pygame.mask.from_surface(self.surface)
        self.rect: pygame.Rect = self.surface.get_rect()
