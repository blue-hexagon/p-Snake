import curses

import menu
import scores
import snake

if __name__ == '__main__':
    while True:
        scores.load_scores()
        curses.wrapper(menu.main)
        curses.wrapper(snake.main)
