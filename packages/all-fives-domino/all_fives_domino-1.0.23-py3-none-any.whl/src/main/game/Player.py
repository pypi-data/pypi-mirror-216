import time

from src.main.config import TARGET_SCORE
from src.main.game.Hand import Hand
from src.main.game.exceptions.Game import GameWinSignal


class Player:
    def __init__(self, brain: "Brain", name: str = None):
        self.hand = Hand()
        self._score = 0
        self.brain = brain
        self.round = None
        self.name = name

    def json(self):
        return {
            "name": self.name,
            "hand": self.hand.json(),
            "score": self.score,
            "brain": self.brain.json()
        }

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value: int):
        self._score = value
        if self.score >= TARGET_SCORE:
            raise GameWinSignal(self)

    def decide(self):
        return self.brain.decide(self, self.round)

    def draw(self):
        piece = self.round.pool.pop()
        self.hand.add(piece)

        if self.round.game.interactive:
            print("Sleeping")
            if self.round.board.origin is None:
                time.sleep(.2)
            else:
                time.sleep(1)
