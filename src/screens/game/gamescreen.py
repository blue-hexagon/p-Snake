import curses
from curses import textpad

from src.screens.abstract_screen import StatefulScreen
from src.screens.game.food_handler import FoodManager
from src.screens.game.obstacle_handler import ObstacleManager
from src.screens.game.pause_screen import PauseScreen
from src.screens.game.snake import Snake
from src.screens.game.snake_keypress_controller import InGameKeyPress
from src.state_management.game_config import GameConfig
from src.state_management.simple_database import SimpleDB as db
from src.utils.key_defs import KeyDefinition as keymap


class GameScreen(StatefulScreen):
    """This class is super ugly and it probably smells"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.food_manager = FoodManager()

    def draw_screen(self) -> None:
        stdscr = GameConfig.get_stdscr()
        stdscr.clear()
        stdscr.refresh()
        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.timeout(GameConfig.get_gamespeed())

        h, w = stdscr.getmaxyx()
        GameConfig.set_h_w(h, w)

        game_canvas = [[3, 3], [h - 3, w - 3]]
        GameConfig.set_canvas_dimensions(game_canvas)

        textpad.rectangle(stdscr, game_canvas[0][0], game_canvas[0][1], game_canvas[1][0], game_canvas[1][1])

        snake = Snake(initial_length=5)
        snake.draw_snake()
        snake.set_direction(curses.KEY_RIGHT)
        current_direction = prev_direction = snake.get_direction()

        obstacles = ObstacleManager().create_obstacles(snake.body)
        food = self.food_manager.create_food(snake.body, obstacles)

        score = 0

        iter_counter = 0

        while True:
            iter_counter += 1
            self.draw_informal_text(iter_counter, snake.body)
            self.print_score(w, score)
            head = snake.body[0]
            key_pressed = stdscr.getch()
            if key_pressed in [curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_UP]:
                prev_direction = current_direction
                current_direction = key_pressed
            elif key_pressed in [keymap.ESCAPE, keymap.LOWER_P]:
                PauseScreen.draw_screen()
            for direction in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
                if current_direction == direction:
                    key_pressed = InGameKeyPress(head).get_keypress_object(direction)
                    snake_symbol_head = key_pressed.snake_symbol_head
                    new_head = key_pressed.new_head
                    snake_symbol_neck = key_pressed.determine_neck_symbol(prev_direction)

            prev_direction = current_direction

            snake.body.insert(0, new_head)  # TODO: How to silence this?
            stdscr.addstr(new_head[0], new_head[1], snake_symbol_head)  # TODO: How to silence this?
            stdscr.addstr(snake.body[1][0], snake.body[1][1], snake_symbol_neck)

            if snake.body[0] == food:
                food = self.food_manager.create_food(snake.body, obstacles)
                score += 1 * len(snake.body)
                self.print_score(w, score)
            elif iter_counter % 100 == 0:
                score += 2 * score // len(snake.body)
                self.print_score(w, score)
            else:
                stdscr.addstr(snake.body[-1][0], snake.body[-1][1], " ")
                snake.body.pop()
            if (
                snake.body[0][0] in [game_canvas[0][0], game_canvas[1][0]]
                or snake.body[0][1] in [game_canvas[0][1], game_canvas[1][1]]
                or snake.body[0] in snake.body[1:]
                or snake.body[0] in obstacles
            ):
                # TODO:
                # db.update_current_players_score(score)
                stdscr.addstr(h // 2, w // 2 - len("GAME OVER") // 2, "GAME OVER")
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
        stdscr.addstr(0, stdscr.getmaxyx()[1] - len("Press ESC or 'p' to pause"), "Press ESC or 'p' to pause")

        """ Draws a string that shows the current players name """
        stdscr.addstr(
            stdscr.getmaxyx()[0] - 1,
            stdscr.getmaxyx()[1] - len(f"Playername: {db.get_player_name()}") - 1,
            f"Playername: {db.get_player_name()}",
        )

    @staticmethod
    def print_score(w, score) -> None:
        stdscr = GameConfig.get_stdscr()
        score_text = f"Score: {score}"
        stdscr.addstr(2, w // 2 - len(score_text) // 2, score_text)
        stdscr.refresh()
