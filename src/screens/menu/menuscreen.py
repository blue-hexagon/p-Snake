import curses
from enum import Enum

from src.screens.abstract_screen import StatefulScreen
from src.screens.canvas import Canvas
from src.screens.game.gamescreen import GameScreen
from src.screens.menu.nested.exits_screen import ExitScreen
from src.screens.menu.nested.scoreboard_screen import ScoreboardScreen
from src.screens.menu.nested.set_playername_screen import SetPlayernameScreen
from src.state_management.simple_database import SimpleDB
from src.utils.key_defs import KeyDefinition


class ScreensEnumeration(Enum):
    PLAY = 0, "Play"
    SET_PLAYER_NAME = 1, "Change Playername"
    SCOREBOARD = 2, "Scoreboard"
    EXIT = 3, "Exit"

    def __init__(self, screen_number, display_name):
        self.screen_number = screen_number
        self.display_name = display_name


class MainScreen(StatefulScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.canvas = Canvas()

    def draw_screen(self, stdscr) -> None:
        curses.curs_set(0)
        curses.color_pair(1)
        # curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        current_row = 0
        self.print_menu(current_row, stdscr)
        while True:
            """Navigate between the rows and act on the current item when pressing enter"""
            key = stdscr.getch()
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_UP and current_row == 0:
                current_row = len(ScreensEnumeration) - 1
            elif key == curses.KEY_DOWN and current_row < len(ScreensEnumeration) - 1:
                current_row += 1
            elif key == curses.KEY_DOWN and current_row == len(ScreensEnumeration) - 1:
                current_row = 0
            elif key == KeyDefinition.NEWLINE:
                if current_row == ScreensEnumeration.PLAY.screen_number:
                    GameScreen().draw_screen(stdscr)
                elif current_row == ScreensEnumeration.SET_PLAYER_NAME.screen_number:
                    SetPlayernameScreen.draw_screen(stdscr)
                elif current_row == ScreensEnumeration.SCOREBOARD.screen_number:
                    ScoreboardScreen.draw_screen(stdscr)
                    stdscr.getch()
                elif current_row == ScreensEnumeration.EXIT.screen_number:
                    ExitScreen.draw_screen(stdscr)
            self.print_menu(current_row, stdscr)

    def print_menu(self, selected_row_idx, stdscr):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        stdscr.addstr(
            h // 2 - len(ScreensEnumeration) // 2 - 2,
            w // 2 - len(f"Welcome to Snake, {SimpleDB.playername}") // 2,
            f"Welcome to Snake, {SimpleDB.playername}",
        )
        for idx, row in enumerate(ScreensEnumeration):
            x = w // 2 - len(row.display_name) // 2
            y = h // 2 - len(ScreensEnumeration) // 2 + idx
            if idx == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row.display_name)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row.display_name)
        stdscr.refresh()
