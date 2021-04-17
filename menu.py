import curses
import os
import sys
from curses import textpad

from scores import scores

menu = ['Play', 'Scoreboard', 'Exit']


def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h // 2 - len(menu) // 2 - 2, w // 2 - len("Welcome to Snake!") // 2, "Welcome to Snake!")
    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()


def print_scoreboard(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    player_name_max_length = 0
    score_column_max_length = 0
    for idx, fields in enumerate(scores):
        if len(str(fields[0])) > player_name_max_length:
            player_name_max_length = len(str(fields[0]))
        if len(str(fields[1])) > score_column_max_length:
            score_column_max_length = len(str(fields[1]))
    for idx, row in enumerate(scores):
        x = w // 2 - player_name_max_length // 2 - score_column_max_length // 2
        y = h // 2 - len(scores) // 2 + idx
        stdscr.addstr(y, x, row[0].ljust(player_name_max_length) + " - " + str(row[1]))
    stdscr.addstr(h // 2 - len(scores) // 2 - 2, w // 2 - len("Scoreboard") // 2, "Scoreboard")
    stdscr.refresh()


if __name__ == '__main__':
    player_name_max_length = 0
    score_entry_max_length = 0
    for idx, fields in enumerate(scores):
        if len(str(fields[0])) > player_name_max_length:
            player_name_max_length = len(str(fields[0]))


def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w // 2 - len(text) // 2
    y = h // 2
    stdscr.addstr(y, x, text)
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # specify the current selected row
    current_row = 0
    # print the menu
    print_menu(stdscr, current_row)
    while 1:
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == len(menu) - 1:
                print_center(stdscr, "Are you sure you want to exit?")
                key = stdscr.getch()
                if key == curses.KEY_ENTER or key in [10, 13]:
                    sys.exit(0)
            elif current_row == 1:
                print_scoreboard(stdscr)
                stdscr.getch()
            elif current_row == 0:
                print_center(stdscr, '')
                break

        print_menu(stdscr, current_row)
