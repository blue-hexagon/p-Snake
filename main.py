import curses

import colors
import menu
import scores
import snake
from os import path

if __name__ == '__main__':
    if not path.exists(scores.FILENAME+".dir"):
        scores.init_shelve()
    else:
        scores.load_scores()
    while True:
        curses.wrapper(menu.main)
        curses.wrapper(snake.main)
