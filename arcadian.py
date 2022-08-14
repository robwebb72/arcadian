import sys
import pygame

from starfield import Starfield
from systemsettings import SystemSettings
from playlist import PlayList
from gamestate import GameState
from menustate import MenuState

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 768
FPS = 30

playlist = PlayList()


def get_hiscore() -> float:
    hiscore: float = 0
    try:
        with open("hiscore.dat") as file:
            contents = file.read()
            hiscore = float(contents)
    except (FileNotFoundError, ValueError):
        pass
    return hiscore


def save_hiscore(score: float) -> None:
    with open("hiscore.dat", "w") as file:
        file.write(f"{score}")


def game_init() -> SystemSettings:
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Arcadian")
    settings: SystemSettings = SystemSettings(screen, clock)
    settings._best_time = get_hiscore()
    return settings


def game_loop(settings: SystemSettings):
    clock = settings.get_clock()
    screen = settings.get_screen()
    starfield = Starfield(200, (SCREEN_WIDTH, SCREEN_HEIGHT))

    
    while settings.app_quit == False:
        dt_sec = clock.tick(FPS) / 1000
        playlist.check()

        if settings.game_state_manager.current_state_activated == False:
            settings.game_state_manager.get_state().initialise()
            settings.game_state_manager.current_state_activated = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings.app_quit = True
                settings.game_state_manager.current_state_activated = False

            if settings.game_state_manager.current_state_activated == False:
                continue
            if hasattr(event, "key"):
                settings.game_state_manager.get_state().handle_input(event.type, event.key)

        if settings.game_state_manager.current_state_activated == False:
            continue
        settings.game_state_manager.get_state().update(dt_sec)
        starfield.update(dt_sec)

        if settings.game_state_manager.current_state_activated == False:
            continue
        screen.fill((0, 0, 30))
        starfield.draw(screen)
        settings.game_state_manager.get_state().draw(screen)
        pygame.display.update()


def game():
    settings = game_init()

    settings.game_state_manager.add_state("game", GameState(settings))
    settings.game_state_manager.add_state("menu", MenuState(settings))
    settings.game_state_manager.set_state("menu")

    playlist.load("music")
    playlist.start()
    game_loop(settings)
    save_hiscore(settings._best_time)
    playlist.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game()
