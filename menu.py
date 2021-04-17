import curses
import os

from cursesmenu import *
from cursesmenu.items import *

menu = {'title' : 'Curses Menu',
        'type' : 'menu',
        'subtitle' : 'A Curses menu in Python'}

option_1 = {'title' : 'Hello World',
            'type' : 'command',
            'command' : 'echo Hello World!'}

menu['options'] = [option_1]

m = CursesMenu(menu)
selected_action = m.display()

if selected_action['type'] != 'exitmenu':
    os.system(selected_action['command'])
if __name__ == "__main__":
    m = CursesMenu(menu)
