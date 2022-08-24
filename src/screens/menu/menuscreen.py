import curses
from enum import Enum

from src.screens.abstract_screen import StatefulScreen
from src.screens.game.gamescreen import GameScreen
from src.screens.menu.nested.exits_screen import ExitScreen
from src.screens.menu.nested.scoreboard_screen import ScoreboardScreen
from src.screens.menu.nested.set_playername_screen import SetPlayernameScreen
from src.state_management.game_config import GameConfig
from src.state_management.simple_database import SimpleDB as db
from src.utils.key_defs import KeyDefinition


class MenuItemsEnumeration(Enum):
    PLAY = 0, "Play"
    SET_PLAYER_NAME = 1, "Change Playername"
    SCOREBOARD = 2, "Scoreboard"
    EXIT = 3, "Exit"

    def __init__(self, row_number, display_name):
        self.row_number = row_number
        self.display_name = display_name


class MainScreen(StatefulScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.stdscr = GameConfig.get_stdscr()
        curses.curs_set(0)
        curses.color_pair(1)
        self.current_row = 0
        self.print_menu()

    def draw_screen(self) -> None:
        while True:
            """Navigate between the rows and act on the current item when pressing enter"""
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_UP and self.current_row == 0:
                self.current_row = len(MenuItemsEnumeration) - 1
            elif key == curses.KEY_DOWN and self.current_row < len(MenuItemsEnumeration) - 1:
                self.current_row += 1
            elif key == curses.KEY_DOWN and self.current_row == len(MenuItemsEnumeration) - 1:
                self.current_row = 0
            elif key == KeyDefinition.NEWLINE:
                if self.current_row == MenuItemsEnumeration.PLAY.row_number:
                    GameScreen().draw_screen()
                elif self.current_row == MenuItemsEnumeration.SET_PLAYER_NAME.row_number:
                    SetPlayernameScreen.draw_screen()
                elif self.current_row == MenuItemsEnumeration.SCOREBOARD.row_number:
                    ScoreboardScreen.draw_screen()
                elif self.current_row == MenuItemsEnumeration.EXIT.row_number:
                    ExitScreen.draw_screen()
            self.print_menu()

    def print_menu(self):
        h, w = self.stdscr.getmaxyx()
        self.stdscr.clear()
        ui_title = f"Welcome to Snake, {db.get_player_name()}"
        self.stdscr.addstr(
            h // 2 - len(MenuItemsEnumeration) // 2 - 2,
            w // 2 - len(ui_title) // 2,
            ui_title,
        )
        for idx, row in enumerate(MenuItemsEnumeration):
            x = w // 2 - len(row.display_name) // 2
            y = h // 2 - len(MenuItemsEnumeration) // 2 + idx
            if idx == self.current_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row.display_name)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row.display_name)
        self.stdscr.refresh()
