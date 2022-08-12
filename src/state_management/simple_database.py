import os.path
import shelve
from os import path
from typing import List


class SimpleDB:
    _ROOT_DIR = os.path.abspath("data/")
    highscores = List[str, int]
    playername = "New Player"
    filename = "highscores"
    filename_extension = ".db"

    def __init__(self) -> None:
        self.initial_highscore_table = [
            ["Blaze", 1000],
            ["Fast Eddy", 900],
            ["Starcat", 800],
            ["Hammerhead", 700],
            ["Mad Hatter", 600],
            ["Primus", 500],
            ["Tempest", 400],
            ["Blackbird", 300],
            ["DragonHawk", 200],
            ["Wonderboy", 100],
        ]
        self.is_initialized = path.exists(self.get_file_path(with_file_extension=True) + ".dir")
        if self.is_initialized:
            self.load_scores()
        else:
            self.init_shelve()

    @staticmethod
    def get_shelve() -> shelve:
        return shelve.open(SimpleDB.get_file_path(with_file_extension=True), writeback=True)

    @classmethod
    def get_filename(cls, with_file_extension=False) -> str:
        if with_file_extension:
            return cls.filename + cls.filename_extension
        else:
            return cls.filename

    @classmethod
    def get_file_path(cls, with_file_extension=False) -> str:
        if with_file_extension:
            return os.path.join(cls._ROOT_DIR, cls.filename + cls.filename_extension)
        else:
            return os.path.join(cls._ROOT_DIR, cls.filename)

    def init_shelve(self) -> None:
        with self.get_shelve() as simple_db:
            for i in range(0, len(self.initial_highscore_table)):
                simple_db[
                    self.get_filename(with_file_extension=False) + f"{'-' + str(i)}"
                    ] = self.initial_highscore_table[i]
            simple_db["playername"] = self.playername
        self.load_scores()

    @classmethod
    def load_scores(cls) -> None:
        with cls.get_shelve() as simple_db:
            cls.highscores.clear()
            for i in range(0, 10):
                cls.highscores.append(simple_db[cls.get_filename(with_file_extension=False) + f"{'-' + str(i)}"])
            cls.playername = simple_db["playername"]

    @classmethod
    def update_playername(cls) -> None:
        with cls.get_shelve() as simple_db:
            simple_db["playername"] = cls.playername

    @classmethod
    def update_score(cls, gamescore) -> None:
        # TODO: This replaces the current entry, it needs to push the entries down one level each for entries with a lower score
        for idx in enumerate(cls.highscores):
            if gamescore >= cls.highscores[idx[0]][1]:
                with shelve.open(cls.get_filename(), writeback=True) as d:
                    d[cls.get_filename(with_file_extension=True) + str(idx[0])][0] = cls.playername
                    d[cls.get_filename(with_file_extension=True) + str(idx[0])][1] = gamescore
                cls.highscores[idx[0]][1] = gamescore
                cls.highscores[idx[0]][0] = cls.playername
                cls.load_scores()
                break
