import curses

import menu
import snake

if __name__ == '__main__':
    while True:
        curses.wrapper(menu.main)
        curses.wrapper(snake.main)
