import curses

from src.screens.abstract_screen import StatelessScreen
from src.state_management.game_config import GameConfig
from src.state_management.simple_database import SimpleDB
from src.utils.key_defs import KeyDefinition


class SetPlayernameScreen(StatelessScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    def draw_screen() -> None:
        stdscr = GameConfig.get_stdscr()
        stdscr.clear()
        counter = 0
        curses.cbreak(True)
        playername = str()
        h, w = stdscr.getmaxyx()
        msg = "What's your name, player?"
        stdscr.addstr(h // 2 - 1, w // 2 - len(msg) // 2, msg)
        while True:
            key = stdscr.getch()
            if key in [KeyDefinition.NEWLINE]:
                curses.cbreak(True)
                SimpleDB.playername = playername
                SimpleDB.update_playername()
                break
            stdscr.addstr(h // 2, w // 2 + counter, chr(key))
            playername += chr(key)
            counter += 1
            stdscr.refresh()
