import pygame


class BaseGameState:
    def state_init(self):
        pass

    def state_update(self, dt_sec : float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass
