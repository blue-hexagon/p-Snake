import curses

from src.screens.abstract_screen import StatelessScreen
from src.state_management.game_config import GameConfig


class PauseScreen(StatelessScreen):
    @staticmethod
    def draw_screen() -> None:
        stdscr = GameConfig.get_stdscr()
        h, w = GameConfig.get_h_w()
        pause_screen_message = "Game Paused"
        stdscr.addstr(h // 2, w // 2 - len(pause_screen_message) // 2, pause_screen_message, curses.A_BLINK)
        stdscr.nodelay(0)
        stdscr.timeout(-1)
        stdscr.getch()
        stdscr.nodelay(1)
        stdscr.timeout(GameConfig.get_gamespeed())
        stdscr.addstr(h // 2, w // 2 - len(pause_screen_message) // 2, " " * len(pause_screen_message))
