from itertools import count
from typing import List


class ListSizeExceededError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__()
        print(msg)


class CounterExceededLimitError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__()
        print(msg)


class RankCounter:
    current_count: int = -1
    iterator = count(start=-1, step=1)

    @classmethod
    def get_next(cls):
        cls.current_count = next(cls.iterator)
        if cls.current_count >= HighscoreTable.TABLE_LENGTH:
            raise CounterExceededLimitError(f"Counter exceeded limit of {HighscoreTable.TABLE_LENGTH}")
        return cls.current_count


class LeaderBoardRank:
    def __init__(self):
        self.ranking: int = -1

    def __str__(self) -> str:
        return str(self.ranking)

    def __repr__(self) -> str:
        return f'LeaderBoardRank("{self.ranking}")'


class Player:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Person("{self.name}")'


class GameScore:
    def __init__(self, score: int) -> None:
        self.score = score

    def __str__(self) -> str:
        return str(self.score)

    def __repr__(self) -> str:
        return f'Score("{self.score}")'


class HighscoreEntry:
    def __init__(self, player: Player, gamescore: GameScore, ranking: LeaderBoardRank) -> None:
        self.leaderboard_rank: LeaderBoardRank = ranking
        self.player: Player = player
        self.score: GameScore = gamescore

    def __str__(self) -> str:
        return f"{self.player}: {self.score}"

    def __repr__(self) -> str:
        return f'HighscoreEntry("{self.leaderboard_rank}","{self.player}","{self.score}"'


class HighscoreTable:
    TABLE_LENGTH = 10

    def __init__(self, entries: List[HighscoreEntry]) -> None:
        self.counter = RankCounter()
        self.entries = entries

    def add_entry(self, entry: HighscoreEntry) -> None:
        if not len(self.entries) < self.TABLE_LENGTH:
            raise ListSizeExceededError("List size cannot be greater than 10")
        entry.leaderboard_rank = self.counter.get_next()
        self.entries.append(entry)

    def remove_entry(self, entry: HighscoreEntry) -> None:
        try:
            self.entries.remove(entry)
        except ValueError:
            print(f"{entry} not found in hs_table")


class InitialGameData:
    @staticmethod
    def get_player():
        return Player("Ivy")

    @staticmethod
    def get_highscores():
        return HighscoreTable(
            [
                HighscoreEntry(
                    Player("Blaze"),
                    GameScore(8192),
                    LeaderBoardRank(),
                ),
                HighscoreEntry(
                    Player("Fast Eddy"),
                    GameScore(4096),
                    LeaderBoardRank(),
                ),
                HighscoreEntry(
                    Player("Starcat"),
                    GameScore(2048),
                    LeaderBoardRank(),
                ),
                HighscoreEntry(
                    Player("Hammerhead"),
                    GameScore(1024),
                    LeaderBoardRank(),
                ),
                HighscoreEntry(
                    Player("Mad Hatter"),
                    GameScore(512),
                    LeaderBoardRank(),
                ),
                HighscoreEntry(
                    Player("Primus"),
                    GameScore(256),
                    LeaderBoardRank(),
                ),
                HighscoreEntry(
                    Player("Tempest"),
                    GameScore(128),
                    LeaderBoardRank(),
                ),
                HighscoreEntry(
                    Player("Blackbird"),
                    GameScore(64),
                    LeaderBoardRank(),
                ),
                HighscoreEntry(
                    Player("DragonHawk"),
                    GameScore(32),
                    LeaderBoardRank(),
                ),
                HighscoreEntry(
                    Player("Wonderboy"),
                    GameScore(16),
                    LeaderBoardRank(),
                ),
            ]
        )
