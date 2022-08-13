import curses
import random
from curses import textpad
from typing import List

from src.screens.abstract_screen import StatefulScreen
from src.screens.game.pause_screen import PauseScreen
from src.screens.game.snake_keypress_controller import InGameKeyPress
from src.state_management.game_config import GameConfig
from src.state_management.simple_database import SimpleDB

GAMESPEED = 150


class GameScreen(StatefulScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    def init_snake():
        stdscr = GameConfig.get_stdscr()
        h, w = GameConfig.get_h_w()
        snake = [
            [h // 2, w // 2 + 2],
            [h // 2, w // 2 + 1],
            [h // 2, w // 2],
            [h // 2, w // 2 - 1],
            [h // 2, w // 2 - 2],
        ]
        for y, x in snake:
            stdscr.addstr(y, x, "─")
        direction = curses.KEY_RIGHT
        return direction, snake

    @staticmethod
    def init_screen():
        stdscr = GameConfig.get_stdscr()
        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.timeout(GAMESPEED)
        h, w = stdscr.getmaxyx()
        game_canvas = [[3, 3], [h - 3, w - 3]]
        GameConfig.set_h_w(h, w)
        GameConfig.set_canvas_dimensions(game_canvas)
        textpad.rectangle(stdscr, game_canvas[0][0], game_canvas[0][1], game_canvas[1][0], game_canvas[1][1])

    def draw_screen(self) -> None:
        stdscr = GameConfig.get_stdscr()
        stdscr.clear()
        stdscr.refresh()
        self.init_screen()
        h, w = GameConfig.get_h_w()
        game_canvas = GameConfig.get_canvas_dimensions()
        current_direction, snake = self.init_snake()
        prev_direction = current_direction
        snake_symbol_neck = "─"
        obstacles = self.create_obstacles(game_canvas, snake)
        food = self.create_food(snake, game_canvas, obstacles)
        score = 0
        iter_counter = 0

        while True:
            iter_counter += 1
            self.draw_informal_text(iter_counter, snake)
            self.print_score(w, score)
            head = snake[0]
            key = stdscr.getch()
            if key in [curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_UP]:
                prev_direction = current_direction
                current_direction = key
            elif key in [27, 112]:  # 'ESC' or 'p'
                PauseScreen.draw_screen(stdscr)
            for direction in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
                if current_direction == direction:
                    key = InGameKeyPress(head).get_keypress_object(direction)
                    snake_symbol_head = key.snake_symbol_head
                    new_head = key.new_head
                    snake_symbol_neck = key.determine_neck_symbol(prev_direction)

            prev_direction = current_direction
            snake.insert(0, new_head)
            stdscr.addstr(new_head[0], new_head[1], snake_symbol_head)
            stdscr.addstr(snake[1][0], snake[1][1], snake_symbol_neck)

            if snake[0] == food:
                food = self.create_food(snake, game_canvas, obstacles)
                score += 1 * len(snake)
                self.print_score(w, score)
            elif iter_counter % 100 == 0:
                score += 2 * score // len(snake)
                self.print_score(w, score)
            else:
                stdscr.addstr(snake[-1][0], snake[-1][1], " ")
                snake.pop()
            if (
                    snake[0][0] in [game_canvas[0][0], game_canvas[1][0]]
                    or snake[0][1] in [game_canvas[0][1], game_canvas[1][1]]
                    or snake[0] in snake[1:]
                    or snake[0] in obstacles
            ):
                msg = "GAME OVER"
                SimpleDB.update_score(score)
                stdscr.addstr(h // 2, w // 2 - len(msg) // 2, msg)
                stdscr.nodelay(0)
                stdscr.timeout(-1)
                stdscr.getch()
                break
            stdscr.refresh()

    @staticmethod
    def draw_informal_text(iter_counter, snake) -> None:
        stdscr = GameConfig.get_stdscr()
        """Draws a string that displays the snakes current position on the gamescreen"""
        stdscr.addstr(0, 0, f"Pos(x,y):{str(snake[0]).replace(']', ' ').replace('[', ' ')}")

        """ Draws a string that displays the current number of gameloops so far """
        stdscr.addstr(stdscr.getmaxyx()[0] - 1, 0, f"Steps: {iter_counter}")

        """ Draws a string that tells the player how to pause the game """
        stdscr.addstr(0, stdscr.getmaxyx()[1] - 20, "Press ESC or 'p' to pause")

        """ Draws a string that shows the current players name """
        player_name_ui_string = f"Playername: {SimpleDB.playername}"
        stdscr.addstr(
            stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - len(player_name_ui_string) - 1, player_name_ui_string
        )

    @staticmethod
    def create_obstacles(game_canvas, snake) -> List[List[int]]:
        stdscr = GameConfig.get_stdscr()
        obstacles: List[List[int]] = []
        while len(obstacles) <= 50:
            obstacles.append(
                [
                    random.randint(game_canvas[0][0] + 3, game_canvas[1][0] - 3),
                    random.randint(game_canvas[0][1] + 3, game_canvas[1][1] - 3),
                ]
            )
            if obstacles in snake:
                obstacles.pop()
            if len(obstacles) > 1:
                if obstacles[-1] in obstacles[-2]:
                    obstacles.pop()
                elif obstacles[-2] in [
                    obstacles[-1][0] - 1,
                    obstacles[-1][0] + 1,
                    obstacles[-1][1] - 1,
                    obstacles[-1][1] + 1,
                    obstacles[-1][0] - 2,
                    obstacles[-1][0] + 2,
                    obstacles[-1][1] - 2,
                    obstacles[-1][1] + 2,
                ]:
                    obstacles.pop()
        stdscr.attron(curses.A_BOLD)
        for idx, coords in enumerate(obstacles):
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(coords[0], coords[1], "#")
        stdscr.attroff(curses.color_pair(4))
        return obstacles

    def create_food(self, snake, game_canvas, obstacles) -> List[int]:
        stdscr = GameConfig.get_stdscr()
        food = None
        while food is None:
            food = [
                random.randint(game_canvas[0][0] + 1, game_canvas[1][0] - 1),
                random.randint(game_canvas[0][1] + 1, game_canvas[1][1] - 1),
            ]
            if food in snake or food in obstacles:
                food = None
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(food[0], food[1], "@")
        stdscr.attroff(curses.A_BOLD)
        stdscr.attroff(curses.color_pair(2))
        return food

    def print_score(self, w, score) -> None:
        stdscr = GameConfig.get_stdscr()
        score_text = f"Score: {score}"
        stdscr.addstr(2, w // 2 - len(score_text) // 2, score_text)
        stdscr.refresh()
