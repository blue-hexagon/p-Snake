import curses
import random
from dataclasses import dataclass
from typing import List

from src.state_management.game_config import GameConfig


@dataclass
class Food:
    x: int
    y: int
    symbol: str = "@"


class FoodManager:
    def __init__(self):
        self.food = None

    def create_food(self, snake, obstacles) -> List[int]:
        """Reset the food item each time create-food is run"""
        self.food = None
        stdscr = GameConfig.get_stdscr()
        game_canvas = GameConfig.get_canvas_dimensions()
        while self.food is None:
            self.food = [
                random.randint(game_canvas[0][0] + 1, game_canvas[1][0] - 1),
                random.randint(game_canvas[0][1] + 1, game_canvas[1][1] - 1),
            ]
            if self.food in snake or self.food in obstacles:
                self.food = None
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(self.food[0], self.food[1], "@")
        stdscr.attroff(curses.A_BOLD)
        stdscr.attroff(curses.color_pair(2))
        return self.food
