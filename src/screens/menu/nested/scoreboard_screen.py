from src.screens.abstract_screen import StatelessScreen
from src.state_management.game_config import GameConfig
from src.state_management.simple_database import SimpleDB


class ScoreboardScreen(StatelessScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    def draw_screen() -> None:
        stdscr = GameConfig.get_stdscr()
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        player_name_max_length = 0
        score_column_max_length = 0
        scoreboard_fs = "  -  "
        for idx, fields in enumerate(SimpleDB.highscores):
            if len(str(fields[0])) > player_name_max_length:
                player_name_max_length = len(str(fields[0]))
            if len(str(fields[1])) > score_column_max_length:
                score_column_max_length = len(str(fields[1]))
        for idx, row in enumerate(SimpleDB.highscores):
            x = w // 2 - player_name_max_length // 2 - score_column_max_length // 2 - len(scoreboard_fs) // 2
            y = h // 2 - len(SimpleDB.highscores) // 2 + idx
            stdscr.addstr(
                y, x, row[0].ljust(player_name_max_length) + scoreboard_fs + str(row[1]).rjust(score_column_max_length)
            )
        stdscr.addstr(h // 2 - len(SimpleDB.highscores) // 2 - 2, w // 2 - len("Scoreboard") // 2, "Scoreboard")
        stdscr.refresh()
