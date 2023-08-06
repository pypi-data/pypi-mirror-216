import pytest

from src.main.game.DominoRound import DominoRound
from src.main.game.Brain import RandomBrain
from src.main.game.Game import Game
from src.main.game.Hand import Hand
from src.main.game.Piece import Piece
from src.main.game.Player import Player


@pytest.fixture
def example_round():
    game = Game(Player(RandomBrain()), Player(RandomBrain()))
    return DominoRound(Player(RandomBrain()), Player(RandomBrain()), game)


@pytest.fixture
def example_round_all_options():
    game = Game(Player(RandomBrain()), Player(RandomBrain()))
    round = DominoRound(Player(RandomBrain()), Player(RandomBrain()), game)
    round.board.origin = Piece(5, 5)
    round.current_player.hand = Hand(
        Piece(5, 0),
        Piece(5, 1),
        Piece(5, 2),
        Piece(5, 3)
    )

    return round
