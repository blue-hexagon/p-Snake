import curses
import random
from typing import List

from src.state_management.game_config import GameConfig


class Obstacle:
    def __init__(self, position: List[int]):
        self.x = position[0]
        self.y = position[1]


class ObstacleManager:
    def __init__(self):
        self.obstacles: List[List[int]] = []

    def create_obstacles(self, snake) -> List[List[int]]:
        stdscr = GameConfig.get_stdscr()
        game_canvas = GameConfig.get_canvas_dimensions()
        obstacles = self.obstacles
        while len(obstacles) <= GameConfig.get_no_of_obstacles():
            obstacle = [
                random.randint(game_canvas[0][0] + 3, game_canvas[1][0] - 3),
                random.randint(game_canvas[0][1] + 3, game_canvas[1][1] - 3),
            ]
            if not self.collision_check(obstacles, snake):
                obstacles.append(obstacle)
        self.draw_obstacles(obstacles, stdscr)
        return obstacles

    def draw_obstacles(self, obstacles, stdscr):
        stdscr.attron(curses.A_BOLD)
        stdscr.attron(curses.color_pair(4))
        for idx, coords in enumerate(obstacles):
            stdscr.addstr(coords[0], coords[1], "#")
        stdscr.attroff(curses.color_pair(4))
        stdscr.attroff(curses.A_BOLD)

    def collision_check(self, obstacle, snake) -> bool:
        if obstacle in snake:
            return True
        if len(self.obstacles) == 1:
            return False
        for idx, obstacle in enumerate(self.obstacles):
            if obstacle in self.obstacles[idx]:
                return True
        return False
