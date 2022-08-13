from abc import ABC, abstractmethod

from src.state_management.game_config import GameConfig


class Screen(ABC):
    def __init__(self, *args, **kwargs) -> None:
        pass

    @staticmethod
    def draw_centered(text) -> None:
        stdscr = GameConfig.get_stdscr()
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
    def draw_screen(self) -> None:
        pass


class StatelessScreen(Screen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    @abstractmethod
    def draw_screen() -> None:
        pass
