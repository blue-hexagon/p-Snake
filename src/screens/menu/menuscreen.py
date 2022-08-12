import curses
import sys

from src.screens.abstract_screen import StatefulScreen
from src.screens.menu.nested.scoreboard_screen import ScoreboardScreen
from src.screens.menu.nested.set_playername_screen import SetPlayernameScreen
from src.state_management.simple_database import SimpleDB


class MainScreen(StatefulScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.menu_items = ["Play", "Set Player Name", "Scoreboard", "Exit"]

    def draw_screen(self, stdscr) -> None:
        def print_menu(selected_row_idx):
            """Print Menu Logic"""
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            stdscr.addstr(
                h // 2 - len(self.menu_items) // 2 - 2,
                w // 2 - len(f"Welcome to Snake, {SimpleDB.playername}") // 2,
                f"Welcome to Snake, {SimpleDB.playername}",
            )
            for idx, row in enumerate(self.menu_items):
                x = w // 2 - len(row) // 2
                y = h // 2 - len(self.menu_items) // 2 + idx
                if idx == selected_row_idx:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, x, row)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, row)
            stdscr.refresh()

        """ Draw Screen Logic """
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        current_row = 0
        print_menu(current_row)
        while True:
            key = stdscr.getch()
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.menu_items) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if current_row == len(self.menu_items) - 1:
                    self.draw_centered(stdscr, "Are you sure you want to exit?")
                    key = stdscr.getch()
                    if key == curses.KEY_ENTER or key in [10, 13]:
                        sys.exit(0)
                elif current_row == 1:
                    SetPlayernameScreen.draw_screen(stdscr)
                elif current_row == 2:
                    ScoreboardScreen.draw_screen(stdscr)
                    stdscr.getch()
                elif current_row == 0:
                    self.draw_centered(stdscr, "")
                    break
            print_menu(current_row)
