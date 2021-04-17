import curses
from curses import textpad
import random

import scores

GAMESPEED = 150


def main(screen):
    game_canvas, h, w = init_screen(screen)
    current_direction, snake = init_snake(screen, h, w)
    prev_direction = current_direction
    snake_symbol_neck = '─'
    food = create_food(snake, screen, game_canvas)
    score = 0
    iter_counter = 0
    print_score(screen, w, score)

    while True:
        iter_counter += 1
        screen.addstr(0, 0, f"Pos(x,y):{str(snake[0]).replace(']', ' ').replace('[', ' ')}")
        screen.addstr(screen.getmaxyx()[0] - 1, 0, f"Steps: {iter_counter}")
        screen.addstr(0, screen.getmaxyx()[1] - 20, f"Press ESC to pause")
        head = snake[0]
        key = screen.getch()
        if key in [curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_UP]:
            prev_direction = current_direction
            current_direction = key
        elif key in [27]:
            msg = 'Game Paused'
            screen.addstr(h // 2, w // 2 - len(msg) // 2, msg, curses.A_BLINK)
            screen.nodelay(0)
            screen.timeout(-1)
            screen.getch()
            screen.nodelay(1)
            screen.timeout(GAMESPEED)
            screen.addstr(h // 2, w // 2 - len(msg) // 2, ' ' * len(msg))
        if current_direction == curses.KEY_RIGHT:
            snake_symbol_head = '─'
            new_head = [head[0], head[1] + 1]
            if prev_direction == curses.KEY_UP:
                snake_symbol_neck = '╭'
            elif prev_direction == curses.KEY_DOWN:
                snake_symbol_neck = '╰'
            elif prev_direction == curses.KEY_LEFT or prev_direction == curses.KEY_RIGHT:
                snake_symbol_neck = '─'
        elif current_direction == curses.KEY_LEFT:
            snake_symbol_head = '─'
            new_head = [head[0], head[1] - 1]
            if prev_direction == curses.KEY_UP:
                snake_symbol_neck = '╮'
            elif prev_direction == curses.KEY_DOWN:
                snake_symbol_neck = '╯'
            elif prev_direction == curses.KEY_LEFT or prev_direction == curses.KEY_RIGHT:
                snake_symbol_neck = '─'
        elif current_direction == curses.KEY_UP:
            snake_symbol_head = '│'
            new_head = [head[0] - 1, head[1]]
            if prev_direction == curses.KEY_UP or prev_direction == curses.KEY_DOWN:
                snake_symbol_neck = '│'
            elif prev_direction == curses.KEY_LEFT:
                snake_symbol_neck = '╰'
            elif prev_direction == curses.KEY_RIGHT:
                snake_symbol_neck = '╯'
        elif current_direction == curses.KEY_DOWN:
            snake_symbol_head = '│'
            new_head = [head[0] + 1, head[1]]
            if prev_direction == curses.KEY_UP or prev_direction == curses.KEY_DOWN:
                snake_symbol_neck = '│'
            elif prev_direction == curses.KEY_LEFT:
                snake_symbol_neck = '╭'
            elif prev_direction == curses.KEY_RIGHT:
                snake_symbol_neck = '╮'
        prev_direction = current_direction
        snake.insert(0, new_head)
        screen.addstr(new_head[0], new_head[1], snake_symbol_head)
        screen.addstr(snake[1][0], snake[1][1], snake_symbol_neck)

        if snake[0] == food:
            food = create_food(snake, screen, game_canvas)
            score += 1 * len(snake)
            print_score(screen, w, score)
        elif iter_counter % 100 == 0:
            score += 2 * score // len(snake)
            print_score(screen, w, score)
        else:
            screen.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()
        if snake[0][0] in [game_canvas[0][0], game_canvas[1][0]] or \
                snake[0][1] in [game_canvas[0][1], game_canvas[1][1]] or \
                snake[0] in snake[1:]:
            msg = 'GAME OVER'
            scores.update_score(score)
            screen.addstr(h // 2, w // 2 - len(msg) // 2, msg)
            screen.nodelay(0)
            screen.timeout(-1)
            screen.getch()
            break
        screen.refresh()


def create_food(snake, screen, game_canvas):
    food = None
    while food is None:
        food = [random.randint(game_canvas[0][0] + 1, game_canvas[1][0] - 1),
                random.randint(game_canvas[0][1] + 1, game_canvas[1][1] - 1)]
        if food in snake:
            food = None
    screen.addstr(food[0], food[1], '*')
    return food


def print_score(screen, w, score):
    score_text = f"Score: {score}"
    screen.addstr(2, w // 2 - len(score_text) // 2, score_text)
    screen.refresh()


def init_snake(screen, h, w):
    snake = [[h // 2, w // 2 + 2], [h // 2, w // 2 + 1], [h // 2, w // 2], [h // 2, w // 2 - 1], [h // 2, w // 2 - 2]]
    for y, x in snake:
        screen.addstr(y, x, '─')
    direction = curses.KEY_RIGHT
    return direction, snake


def init_screen(screen):
    curses.curs_set(0)
    screen.nodelay(1)
    screen.timeout(GAMESPEED)
    h, w = screen.getmaxyx()
    game_canvas = [[3, 3], [h - 3, w - 3]]
    textpad.rectangle(screen, game_canvas[0][0], game_canvas[0][1], game_canvas[1][0], game_canvas[1][1])
    return game_canvas, h, w
