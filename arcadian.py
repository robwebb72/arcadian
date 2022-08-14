import sys

import pygame

import colours
import hiscore
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
    game_state_manager = settings.game_state_manager
    starfield = Starfield(200, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while settings.app_quit == False:
        dt_sec = clock.tick(FPS) / 1000
        playlist.check()

        if game_state_manager.current_state_activated == False:
            game_state_manager.get_state().initialise()
            game_state_manager.current_state_activated = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings.app_quit = True
                game_state_manager.current_state_activated = False

            if game_state_manager.current_state_activated == False:
                continue
            if hasattr(event, "key"):
                game_state_manager.get_state().handle_input(event.type, event.key)

        if game_state_manager.current_state_activated == False:
            continue
        settings.game_state_manager.get_state().update(dt_sec)
        starfield.update(dt_sec)

        if game_state_manager.current_state_activated == False:
            continue
        screen.fill(colours.DARK_BLUE)
        starfield.draw(screen)
        game_state_manager.get_state().draw(screen)
        pygame.display.update()


def game():
    settings = game_init()

    settings.game_state_manager.add_state("game", GameState(settings))
    settings.game_state_manager.add_state("menu", MenuState(settings))
    settings.game_state_manager.set_state("menu")
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
