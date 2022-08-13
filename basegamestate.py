import pygame
import typing


class BaseGameState:
    def state_init(self):
        pass

    def initialise(self) -> None:
        pass

    def update(self, dt_sec: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass

    def handle_input(self, type: int, key: int) -> None:
        pass

    def print(
        self,
        screen: pygame.Surface,
        message: str,
        x: int,
        y: int,
        colour: typing.Tuple[int, int, int],
    ) -> None:
        print_surface = self._system_settings.get_font().render(message, True, colour)
        print_rect = print_surface.get_rect()
        print_rect.center = (x, y)
        screen.blit(print_surface, print_rect)

    def create_time_str(self, time: float) -> str:
        milliseconds_string = f"{int(time * 10)% 10}"
        seconds_string = f"{(int(time) % 60):0>2}"
        minutes_string = f"{(int(time / 60) % 60):0>2}"
        hours_string = f"{(int(time / 3600)):0>2}"
        return f"{hours_string}:{minutes_string}:{seconds_string}.{milliseconds_string}"
