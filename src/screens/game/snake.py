import curses

from src.state_management.game_config import GameConfig


class Snake:
    def __init__(self, initial_length=5):
        self.stdscr = GameConfig.get_stdscr()
        h, w = GameConfig.get_h_w()
        self.body = []
        self.direction = curses.KEY_RIGHT
        for x in range(-initial_length // 2 + 1, initial_length // 2 + 1):
            self.body.append([h // 2, w // 2 + x])
        self.body.reverse()

    def draw_snake(self):
        for y, x in self.body:
            self.stdscr.addstr(y, x, "─")

    def set_direction(self, direction: int):
        self.direction = direction

    def get_direction(self):
        return self.direction
