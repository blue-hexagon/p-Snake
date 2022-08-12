import curses
import sys

from src.screens.abstract_screen import StatelessScreen
from src.utils.key_defs import KeyDefinition


class ExitScreen(StatelessScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def draw_screen(stdscr):
        StatelessScreen.draw_centered(stdscr, "Are you sure you want to exit?")
        key = stdscr.getch()
        if key != KeyDefinition.NEWLINE:
            return
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        sys.exit(0)
