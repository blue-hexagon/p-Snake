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
        field_seperator = "  -  "
        SimpleDB.get_highscore_table()
        """ Create a dynamically sized table with proper padding
            If one of the names become SuperStarcatStarBlazer, or
            a score increases to 131072, the table dynamically
            resizes and aligns all entries.
            Example:
            Blaze       -  8192
            Fast Eddy   -  4096
            Starcat     -  2048
            Hammerhead  -  1024
            Mad Hatter  -   512
            Primus      -   256
            Tempest     -   128
            Blackbird   -    64
            DragonHawk  -    32 """
        for idx, fields in enumerate(SimpleDB.get_highscore_table()):
            if len(str(fields.player.name)) > player_name_max_length:
                player_name_max_length = len(str(fields.player.name))
            if len(str(fields.score)) > score_column_max_length:
                score_column_max_length = len(str(fields.score))
        for idx, entry in enumerate(SimpleDB.get_highscore_table()):
            x = w // 2 - player_name_max_length // 2 - score_column_max_length // 2 - len(field_seperator) // 2
            y = h // 2 - len(SimpleDB.get_highscore_table()) // 2 + idx
            stdscr.addstr(
                y,
                x,
                f"{entry.leaderboard_rank.ranking}. {entry.player.name.ljust(player_name_max_length)} {field_seperator} {str(entry.score).rjust(score_column_max_length)}",
            )
        stdscr.addstr(
            h // 2 - len(SimpleDB.get_highscore_table()) // 2 - 2, w // 2 - (len("Scoreboard") - 7) // 2, "Scoreboard"
        )
        stdscr.refresh()
        stdscr.getch()
