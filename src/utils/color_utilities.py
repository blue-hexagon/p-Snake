import curses


class ColorUtils:
    @staticmethod
    def USE_BLACK_ON_WHITE() -> None:
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    @staticmethod
    def USE_RED_ON_BLACK() -> None:
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    @staticmethod
    def USE_BLUE_ON_BLACK() -> None:
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    @staticmethod
    def USE_GREEN_ON_BLACK() -> None:
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    @staticmethod
    def USE_CYAN_ON_BLACK() -> None:
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)

    @staticmethod
    def USE_MAGENTA_ON_BLACK() -> None:
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    @staticmethod
    def USE_YELLOW_ON_BLACK() -> None:
        curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)
