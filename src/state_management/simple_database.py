import os.path
import shelve
from os import path


class SimpleDB:
    _ROOT_DIR = os.path.abspath("data/")
    highscores = []
    playername = "Ivy"
    filename = "highscores"
    initial_highscore_table = [
        ["Blaze", 8192],
        ["Fast Eddy", 4096],
        ["Starcat", 2048],
        ["Hammerhead", 1024],
        ["Mad Hatter", 512],
        ["Primus", 256],
        ["Tempest", 128],
        ["Blackbird", 64],
        ["DragonHawk", 32],
        ["Wonderboy", 16],
    ]

    def __init__(self) -> None:
        self.is_initialized = path.exists(self.get_file_path() + ".dir")
        if self.is_initialized:
            self.load_scores()
        else:
            self.init_shelve()

    @staticmethod
    def get_shelve() -> shelve:
        return shelve.open(SimpleDB.get_file_path(), writeback=True)

    @classmethod
    def get_filename(cls) -> str:
        return cls.filename

    @classmethod
    def get_file_path(cls) -> str:
        return os.path.join(cls._ROOT_DIR, cls.filename)

    @classmethod
    def init_shelve(cls) -> None:

        with cls.get_shelve() as simple_db:
            for i in range(0, len(cls.initial_highscore_table)):
                simple_db["score-" + str(i)] = cls.initial_highscore_table[i]
            simple_db["playername"] = cls.playername
        cls.load_scores()

    @classmethod
    def load_scores(cls) -> None:
        with cls.get_shelve() as simple_db:
            cls.highscores.clear()
            for i in range(0, len(cls.initial_highscore_table)):
                cls.highscores.append(simple_db["score-" + str(i)])
            cls.playername = simple_db["playername"]

    @classmethod
    def update_playername(cls) -> None:
        with cls.get_shelve() as simple_db:
            simple_db["playername"] = cls.playername

    @classmethod
    def update_score(cls, gamescore: int) -> None:
        # TODO: This replaces the current entry, it needs to push the entries down one level each for entries with a lower score
        for idx in enumerate(cls.highscores):
            if gamescore >= cls.highscores[idx[0]][1]:
                with cls.get_shelve() as simple_db:
                    simple_db["score-" + str(idx[0])] = [cls.playername, gamescore]
                cls.highscores[idx[0]][1] = gamescore
                cls.highscores[idx[0]][0] = cls.playername
                cls.load_scores()
                break
