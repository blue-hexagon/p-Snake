from abc import ABC, abstractmethod


class Screen(ABC):
    def __init__(self, *args, **kwargs) -> None:
        pass

    @staticmethod
    def draw_centered(stdscr, text) -> None:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        x = w // 2 - len(text) // 2
        y = h // 2
        stdscr.addstr(y, x, text)
        stdscr.refresh()


class StatefulScreen(Screen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @abstractmethod
    def draw_screen(self, stdscr) -> None:
        pass


class StatelessScreen(Screen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    @abstractmethod
    def draw_screen(stdscr) -> None:
        pass
