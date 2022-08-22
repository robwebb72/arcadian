import sys

import pygame

import colours
import hiscore
from gamestate_manager import (
    add_state,
    get_state,
    set_state,
    set_current_state_active,
    current_state_is_active as state_is_active,
)
from gamestate import GameState
from menustate import MenuState
from playlist import PlayList
from starfield import Starfield
from systemsettings import SystemSettings

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 768
FPS = 30

playlist = PlayList()


def game_init() -> SystemSettings:
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Arcadian")
    return SystemSettings(screen, clock)


def game_loop(settings: SystemSettings):
    clock = settings.get_clock()
    screen = settings.get_screen()
    starfield = Starfield(200, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while settings.app_quit is False:
        dt_sec = clock.tick(FPS) / 1000
        playlist.check()

        if state_is_active() is False:
            get_state().initialise()
            set_current_state_active(True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings.app_quit = True
                set_current_state_active(False)

            if state_is_active() is False:
                continue
            if hasattr(event, "key"):
                get_state().handle_input(event.type, event.key)

        if state_is_active() is False:
            continue
        get_state().update(dt_sec)
        starfield.update(dt_sec)

        if state_is_active() is False:
            continue
        screen.fill(colours.DARK_BLUE)
        starfield.draw(screen)
        get_state().draw(screen)
        pygame.display.update()


def game():
    settings = game_init()

    add_state("game", GameState(settings))
    add_state("menu", MenuState(settings))
    set_state("menu")
    settings._best_time = hiscore.load()
    playlist.load("music")
    playlist.start()
    game_loop(settings)
    hiscore.save(settings._best_time)
    playlist.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game()
