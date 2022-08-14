from pygame import Surface


class GameStateInterface:
    def __init__(self) -> None:
        pass

    def update(self, dt_sec: float) -> None:
        pass

    def draw(self, screen: Surface) -> None:
        pass
