import curses

from src.screens.menu.menuscreen import MainScreen
from src.state_management.simple_database import SimpleDB
from src.utils.color_utilities import ColorPairInitializer


class Runner:
    """
    For whatever reason curses.KEY_ENTER (int 343) does not work when hitting Enter.
    Hitting Enter returns (int 10) - therefore, whenever an Enter key is expected in the codebase, int 10 is used to check for that key.
    """

    def __init__(self) -> None:
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        ColorPairInitializer()
        SimpleDB()

    def run(self) -> None:
        while True:
            MainScreen().draw_screen(self.stdscr)
