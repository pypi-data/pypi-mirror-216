from src.main.game.Brain import AllFivesGreedyBrain
from src.main.game.Piece import Piece

from src.test.game.fixtures import example_round_all_options


def test_greedy_brain_does_not_alter(example_round_all_options):
    piece, origin, close = AllFivesGreedyBrain().decide(example_round_all_options)

    assert example_round_all_options.board.get_pieces() == [Piece(5, 5)]