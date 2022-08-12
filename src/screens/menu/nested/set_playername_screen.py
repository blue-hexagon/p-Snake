import curses

from src.screens.abstract_screen import StatelessScreen
from src.state_management.simple_database import SimpleDB


class SetPlayernameScreen(StatelessScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    def draw_screen(stdscr) -> None:
        stdscr.clear()
        counter = 0
        curses.cbreak(True)
        key = None
        playername = str()
        h, w = stdscr.getmaxyx()
        msg = "What's your name, player?"
        stdscr.addstr(h // 2 - 1, w // 2 - len(msg) // 2, msg)
        while True:
            key = stdscr.getch()
            if key in [curses.KEY_ENTER, 10, 13]:
                curses.cbreak(True)
                SimpleDB.playername = playername
                SimpleDB.update_playername()
                break
            stdscr.addstr(h // 2, w // 2 + counter, chr(key))
            playername += chr(key)
            counter += 1
            stdscr.refresh()
