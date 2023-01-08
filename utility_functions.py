from pygame import Surface, font
from typing import Tuple


def print(
    screen: Surface,
    font_obj: font.Font,
    message: str,
    x: int,
    y: int,
    colour: Tuple[int, int, int],
) -> None:
    if font_obj is None:
        font_obj = font.SysFont()
    print_surface = font_obj.render(message, True, colour)
    print_rect = print_surface.get_rect()
    print_rect.center = (x, y)
    screen.blit(print_surface, print_rect)


def create_time_str(time: float) -> str:
    ms_string = f"{int(time * 10)% 10}"
    sec_string = f"{(int(time) % 60):0>2}"
    min_string = f"{(int(time / 60) % 60):0>2}"
    hrs_string = f"{(int(time / 3600)):0>2}"
    return f"{hrs_string}:{min_string}:{sec_string}.{ms_string}"
