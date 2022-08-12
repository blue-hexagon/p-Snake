import curses

from src.screens.game.gamescreen import GameScreen
from src.screens.menu.menuscreen import MainScreen
from src.state_management.simple_database import SimpleDB


class Runner:
    def __init__(self) -> None:
        self.gs = SimpleDB()
        self.main_screen = MainScreen()
        self.game_screen = GameScreen()

    def run(self) -> None:
        while True:
            curses.wrapper(self.main_screen.draw_screen)
            curses.wrapper(self.game_screen.draw_screen)
