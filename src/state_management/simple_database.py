import os.path
import shelve
from os import path

from src.state_management.models import (
    GameScore,
    HighscoreEntry,
    HighscoreTable,
    InitialGameData,
    LeaderBoardRank,
    Player,
)


class SimpleDB:
    _dir = os.path.abspath("data/")
    _filename = "highscores"

    def __init__(self) -> None:
        if not path.exists(self.get_file_path() + ".dir"):
            self.init_shelve()

    @classmethod
    def get_file_path(cls) -> str:
        return os.path.join(cls._dir, cls._filename)

    @staticmethod
    def get_shelve() -> shelve:
        return shelve.open(SimpleDB.get_file_path(), writeback=True)

    @classmethod
    def get_player_name(cls):
        with cls.get_shelve() as db:
            player_name = db["player"]
        return player_name

    @classmethod
    def init_shelve(cls) -> None:
        with cls.get_shelve() as db:
            for i in range(0, HighscoreTable.TABLE_LENGTH):
                """score-6 = [Player('Tempest'), GameScore(128)]"""
                entry = InitialGameData.get_highscores().entries[i]
                entry.leaderboard_rank.leaderboard_rank = i
                db["score-" + str(i)] = InitialGameData.get_highscores().entries[i]
            db["player"] = InitialGameData.get_player()

    @classmethod
    def update_playername(cls, player: Player) -> None:
        with cls.get_shelve() as db:
            db["player"] = player.name

    @classmethod
    def get_highscore_table(cls):
        with cls.get_shelve() as db:
            table = []
            for x in range(0, HighscoreTable.TABLE_LENGTH - 1):
                table.append(db[f"score-{x}"])
            return table

    @classmethod
    def update_current_players_score(cls, gamescore: int) -> None:
        # TODO: This replaces the current entry, it needs to push the entries down one level each for entries with a lower score
        for idx in enumerate(cls._highscore_table):
            if gamescore >= cls._highscore_table[idx[0]][1]:
                with cls.get_shelve() as db:
                    db["score-" + str(idx[0])] = [cls._player, gamescore]
                cls._highscore_table[idx[0]][1] = gamescore
                cls._highscore_table[idx[0]][0] = cls._player
                cls.load_scores()
                break
