import curses

from src.screens.canvas import Canvas
from src.screens.game.gamescreen import GameScreen
from src.screens.menu.menuscreen import MainScreen
from src.state_management.simple_database import SimpleDB
from src.utils.color_utilities import ColorPairInitializer


class Runner:
    def __init__(self) -> None:
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.start_color()
        SimpleDB()
        ColorPairInitializer()
        canvas = Canvas()
        self.screens = [
            MainScreen(canvas),
            GameScreen(canvas)
        ]

    def run(self) -> None:
        while True:
            for screen in self.screens:
                screen.draw_screen(self.stdscr)
