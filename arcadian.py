import sys
import typing

import pygame

import colours
from asteroid import AsteroidField
from player import Player
from starfield import Starfield
from systemsettings import SystemSettings

from gamestate import GameState
from menustate import MenuState

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 768
FPS = 30

game_states = {}

def get_hiscore() -> float:
    hiscore:float = 0
    try:
        with open('hiscore.dat') as file:
            contents = file.read()
            hiscore = float(contents)
    except FileNotFoundError:
        pass
    except ValueError:
        pass  
    return hiscore

def save_hiscore(score:float) -> None:
    with open('hiscore.dat','w') as file:
        file.write(f'{score}')

def game_init() -> SystemSettings:
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Arcadian")
    settings :SystemSettings = SystemSettings(screen, clock)
    settings._best_time = get_hiscore()
    return settings


def game_loop(settings: SystemSettings):
    clock = settings.get_clock()
    screen = settings.get_screen()
    starfield = Starfield(200, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while settings.get_state() != "exit":
        dt_sec = clock.tick(FPS) / 1000

        if settings.get_init_state():
            game_states[settings.get_state()].initialise()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings.set_state("exit")
                settings.set_init_state(True)

            if settings.get_init_state():
                continue
            if hasattr(event, "key"):
                game_states[settings.get_state()].handle_input(event.type, event.key)

        if settings.get_init_state():
            continue
        game_states[settings.get_state()].update(dt_sec)
        starfield.update(dt_sec)

        if settings.get_init_state():
            continue
        screen.fill(colours.BLACK)
        starfield.draw(screen)
        game_states[settings.get_state()].draw(screen)
        pygame.display.update()


def game():
    settings = game_init()
    game_states["game"] = GameState(settings)
    game_states["menu"] = MenuState(settings)
    settings.set_state("menu")
    settings.set_init_state(True)
    game_loop(settings)
    save_hiscore(settings._best_time)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game()
